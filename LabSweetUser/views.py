import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Job, Test, Sample, Attribute
from .serializers import SampleSerializer, JobSerializer


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
            test_obj = Test.objects.create(
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
def getSamples(request):
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
def getSample(request, pk):
    try:
        sample = Sample.objects.get(id=pk)
        sample_json = SampleSerializer(sample)
        return Response(sample_json.data)
    except Sample.DoesNotExist:
        return Response({"error": "Sample not found"})


# API to return multiple Jobs
@api_view(['GET'])
def getJobs(request):
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
def getJob(request, job_number):
    job = Job.objects.get(job_number=job_number)
    samples = Sample.objects.filter(user=request.user).filter(job=job)

    if samples:
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)
    error = {'error': 'Job not found'}
    return Response(error)
