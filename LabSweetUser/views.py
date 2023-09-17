import json
import os
import csv
from django import forms
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect, JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Job, Test, Sample, Attribute, Worklist
from .serializers import (
    SampleSerializer,
    JobSerializer,
    WorklistSerializer,
)


class UploadFileForm(forms.Form):
    file = forms.FileField()


@login_required
def index(request):
    return render(request, "LabSweetUser/index.html")


# Creates a sample for each sample in the request and create
# Creates the tests for each sample
# Creates a job to be associated with all the samples in the submission
@login_required
def submit_sample(request):
    data = json.loads(request.body)
    job = Job.create()
    for sample in data:
        sample_id = sample.get("sampleId")
        batch = sample.get("batch")
        tests = sample.get("tests")

        sample = Sample.objects.create(
            user=request.user, sample_id=sample_id, batch=batch, job=job
        )

        for test in tests:
            attribute = Attribute.objects.get(name=test)
            Test.objects.create(sample=sample, attribute=attribute)

    return JsonResponse({"content": "Submitted successfully!"})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "LabSweetUser/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "LabSweetUser/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "LabSweetUser/register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "LabSweetUser/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "LabSweetUser/register.html")


# Marks a sample as complete by checking if all associated
# tests have results
def check_sample_complete(sample):
    for test in sample.tests.all():
        if not test.result:
            return
    sample.complete = True
    sample.save()
    return


# Marks a job as complete if all samples are complete
def check_job_complete(job):
    for sample in job.samples.all():
        if not sample.complete:
            return
    job.complete = True
    job.save()
    return


# API to return multiple samples
@api_view(["GET"])
def get_samples(request):
    samples = Sample.objects.all()
    if not request.user.is_staff:
        samples = samples.filter(user=request.user)
    filter = request.GET.get("filter", None)

    if samples:
        for sample in samples:
            if sample.complete is False:
                check_sample_complete(sample)

        if filter == "Outstanding":
            samples = samples.filter(complete=False)
        elif filter == "Complete":
            samples = samples.filter(complete=True)

    if samples:
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)

    error = {"error": "No samples found"}
    return Response(error)


# API to return a single sample
@api_view(["GET"])
def get_sample(request, pk):
    try:
        sample = Sample.objects.get(id=pk)
        sample_json = SampleSerializer(sample)
        return Response(sample_json.data)
    except Sample.DoesNotExist:
        return Response({"error": "Sample not found"})


# API to return multiple Jobs
@api_view(["GET"])
def get_jobs(request):
    samples = Sample.objects.all()
    if not request.user.is_staff:
        samples = samples.filter(user=request.user)

    job_ids = samples.values("job").distinct()
    jobs = Job.objects.filter(id__in=job_ids)
    filter = request.GET.get("filter", None)

    if jobs:
        for job in jobs:
            if job.complete is False:
                check_job_complete(job)

        if filter == "Outstanding":
            jobs = jobs.filter(complete=False)
        elif filter == "Complete":
            jobs = jobs.filter(complete=True)

    if jobs:
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    error = {"error": "No jobs found"}
    return Response(error)


# API to return a single Job
@api_view(["GET"])
def get_job(request, job_number):
    job = Job.objects.get(job_number=job_number)
    samples = Sample.objects.filter(job=job)
    if not request.user.is_staff:
        samples = samples.filter(user=request.user)

    if samples:
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)
    error = {"error": "Job not found"}
    return Response(error)


# API to return all existing worklists
@api_view(["GET"])
def get_worklists(request):
    filter = request.GET.get("filter", None)
    worklists = Worklist.objects.all()

    if worklists:
        if filter == 'Outstanding':
            worklists = worklists.filter(tests__result__isnull=True).distinct()
        elif filter == 'Complete':
            worklists = worklists.filter(tests__result__isnull=False).distinct()

    if worklists:
        serializer = WorklistSerializer(worklists, many=True)
        return Response(serializer.data)

    error = {"error": "No worklists found"}
    return Response(error)


@staff_member_required
def staff_view(request):
    return render(request, "LabSweetUser/staff_view.html")


# API to return attributes that have outstanding tests,
# and a count of those tests
@staff_member_required
@api_view(["GET"])
def outstanding_work_view(request):
    attributes = Attribute.objects.all()
    outstanding_tests = []
    for attribute in attributes:
        test_count = (
            Test.objects.filter(attribute=attribute).filter(worklist=None).count()
        )
        if test_count > 0:
            outstanding_tests.append(
                {
                    "name": attribute.name,
                    "full_name": attribute.full_name,
                    "test_count": test_count,
                }
            )

    if outstanding_tests:
        return Response(outstanding_tests)

    error = {"error": "No outstanding tests"}
    return Response(error) 


# API to create a worklist for a given attribute out of tests that have not
# been assigned a worklist
@api_view(["PUT"])
def generate_worklist(request, attribute):
    tests = Test.objects.filter(attribute__name=attribute).filter(worklist=None)

    if tests:
        if request.method == "PUT":
            worklist = Worklist.create()
            for test in tests:
                test.worklist = worklist
                test.save()
            serializer = WorklistSerializer(worklist)
            return Response(serializer.data)

    error = {"error": f"No outstanding {test} tests"}
    return Response(error)


# API to create a csv file of tests in a given worklist if the
# file doesn't already exist, and download the csv file
@api_view(["GET"])
def download_worklist(request, worklist_number):
    tests = Test.objects.filter(worklist__worklist_number=worklist_number)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = BASE_DIR + "/LabSweetUser/static/worklists/" + worklist_number + ".csv"

    if not os.path.exists(filepath):
        with open(filepath, "w", newline="") as file:
            writer = csv.writer(file)
            headers = [
                "LIMS ID",
                "Sample ID",
                "Batch",
                f"{tests[0].attribute.full_name} Result ({tests[0].attribute.units})",
            ]

            writer.writerow(headers)
            for test in tests:
                writer.writerow([test.id, test.sample.sample_id, test.sample.batch])

    response = FileResponse(open(filepath, "rb"))

    # Set the content-disposition header to trigger a file download prompt
    response["Content-Disposition"] = "attachment;"

    return response


# Get the test results from a csv file and save them to each test
def upload_results(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            results = file.read().decode("utf-8")
            reader = csv.reader(
                results.splitlines(),
                dialect="excel",
                delimiter=","
            )
            next(reader, None)
            for row in reader:
                test_id = row[0]
                result = row[3]
                test = Test.objects.get(id=test_id)
                test.result = result
                test.save()

            return HttpResponseRedirect(reverse("staff"))
    else:
        form = UploadFileForm()
        return render(request, "LabSweetUser/upload_results.html", {"form": form})
