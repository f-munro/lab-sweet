import json
import os
import csv
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Job, Test, Sample, Attribute, Worklist
from .serializers import SampleSerializer, JobSerializer, TestSerializer

#   To Do
#   -   Make 'staff' link, only visible if 'is_staff'
#   -   Func to write an outstanding worklist to a file. Might be best to conv.
#       a queryset to a dict, with Test.objects.all().values("field1","field2")
#       and use csv dictwriter to write to a file


if not Attribute.objects.all():
    Attribute.create_table()


@login_required
def index(request):
    return render(request, 'LabSweetUser/index.html')


@login_required
def submit_sample(request):
    data = json.loads(request.body)
    job = Job.create()
    for sample in data:
        sample_id = sample.get("sampleId")
        batch = sample.get("batch")
        tests = sample.get("tests")

        sample = Sample.objects.create(
            user=request.user,
            sample_id=sample_id,
            batch=batch,
            job=job
        )

        for test in tests:
            attribute = Attribute.objects.get(name=test)
            Test.objects.create(
                sample=sample,
                attribute=attribute
            )

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
            return render(request, "LabSweetUser/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "LabSweetUser/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "LabSweetUser/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "LabSweetUser/register.html")


def check_sample_complete(sample):
    for test in sample.tests.all():
        if not test.result:
            return
    sample.complete = True
    sample.save()
    return


def check_job_complete(job):
    for sample in job.samples.all():
        if not sample.complete:
            return
    job.complete = True
    job.save()
    return


# API to return multiple samples
@api_view(['GET'])
def get_samples(request):
    samples = Sample.objects.filter(user=request.user)
    filter = request.GET.get("filter", None)

    if samples:
        for sample in samples:
            if sample.complete is False:
                check_sample_complete(sample)

        if filter == 'Outstanding':
            samples = samples.filter(complete=False)
        elif filter == 'Complete':
            samples = samples.filter(complete=True)

    if samples:
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)

    error = {'error': 'No samples found'}
    return Response(error)


# API to return a single sample
@api_view(['GET'])
def get_sample(request, pk):
    try:
        sample = Sample.objects.get(id=pk)
        sample_json = SampleSerializer(sample)
        return Response(sample_json.data)
    except Sample.DoesNotExist:
        return Response({"error": "Sample not found"})


# API to return multiple Jobs
@api_view(['GET'])
def get_jobs(request):
    samples = Sample.objects.filter(user=request.user)
    job_ids = samples.values('job').distinct()
    jobs = Job.objects.filter(id__in=job_ids)
    filter = request.GET.get("filter", None)

    if jobs:
        for job in jobs:
            if job.complete is False:
                check_job_complete(job)

        if filter == 'Outstanding':
            jobs = jobs.filter(complete=False)
        elif filter == 'Complete':
            jobs = jobs.filter(complete=True)

    if jobs:
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    error = {'error': "No jobs found"}
    return Response(error)


# API to return a single Job
@api_view(['GET'])
def get_job(request, job_number):
    job = Job.objects.get(job_number=job_number)
    samples = Sample.objects.filter(user=request.user).filter(job=job)

    if samples:
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)
    error = {'error': 'Job not found'}
    return Response(error)


# Function to allow user to download a csv template:
@staff_member_required
def download_template(request):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = BASE_DIR + '/LabSweetUser/static/styles.css'

    # Set the response content type to plain text file
    response = FileResponse(open(filepath, 'rb'))

    # Set the content-disposition header to trigger a file download prompt
    response['Content-Disposition'] = 'attachment; filename="results_template.csv"'

    return response


def staff_view(request):
    return render(request, "LabSweetUser/outstanding_work.html")


@api_view(['GET'])
def outstanding_work_view(request):
    attributes = Attribute.objects.all()
    outstanding_tests = []
    for attribute in attributes:
        test_count = Test.objects.filter(attribute=attribute).filter(worklist=None).count()
        if test_count > 0:
            outstanding_tests.append({"name": attribute.name,
                                      "full_name": attribute.full_name,
                                      "test_count": test_count})

    return Response(outstanding_tests)


@api_view(['PUT'])
def generate_worklist(request, test):
    tests = Test.objects.filter(attribute__name=test).filter(worklist=None)

    if tests:
        if request.method == 'PUT':
            worklist = Worklist.create()
            for test in tests:
                test.worklist = worklist
                test.save()
            serializer = TestSerializer(tests, many=True)
            return Response(serializer.data)

    error = {'error': f"No outstanding {test} tests"}
    return Response(error)


def download_worklist(request, test):
    # Get the chosen tests as a dictionary
    # tests = Test.objects.filter(attribute=test).values()
    tests = Test.objects.filter(attribute__id=test)
    test = tests[0]
    print(f"Attribute:{test.attribute.name}")
    print(f"sample:{test.sample.job.job_number}")
    
    return HttpResponse("Done")
'''    with open('profiles1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["name", "age", "country"]

        writer.writerow(field)
        writer.writerow(["Oladele Damilola", "40", "Nigeria"])
        writer.writerow(["Alina Hricko", "23", "Ukraine"])
        writer.writerow(["Isabel Walter", "50", "United Kingdom"])
        
        click a test -> generates a w/l
        call both outstandingWork and generateWorklist
        click dl button -> dl's the w/l and clears the table
        '''

