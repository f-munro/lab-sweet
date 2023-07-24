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
from .serializers import JobSerializer, TestSerializer, SampleSerializer

'''
                    _+_+_+_+_+_+_+__TO DO__+_+_+_+_+_+_+_
    X   Clicking on a job shows samples. When a sample is clicked from here,
        should show the sample view
    X   selecting 'complete jobs' doesn't work
    X   Sort the HTML for search box. Add one to search for jobs too.
    X   Need to sort out 'complete' status for everything. Job, samples and
        tests all have a 'complete' field in the model. How to make
        samples/jobs complete. Should jobs have a % complete column
    X   test outstanding samples works
    X   Latest samples/All samples?
    X   Sort sub form boxes - use one kind of label
    X   Make a homepage?
    X   Add jobs back in but change "get_job" to return from samples instead of jobs


job = Job.objects.first()
samples = job.tests.values('sample').distinct().count()
tests = job.tests.count()
progress = job.tests.filter(completed=True).count()
progress_percent = int(progress / tests * 100)
print(f"Samples: {samples}")
print(f"Completed: {tests}")
print(f"Progress: {progress}/{tests}")
print(f"Progress Percent: {progress_percent}%")
'''


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


# API to return multiple samples
@api_view(['GET'])
def getSamples(request):
    samples = Sample.objects.filter(user=request.user)
    filter = request.GET.get("filter", None)
    if filter == 'Outstanding':
        samples = samples.filter(complete=False)
    elif filter == 'Complete':
        samples = samples.filter(complete=True)

    if samples:
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)

    error = {'error': f'You have no {filter} samples'}
    return Response(error)


# API to return multiple Jobs
@api_view(['GET'])
def getJobs(request):
    samples = Sample.objects.filter(user=request.user)
    job_ids = samples.values('job').distinct()
    jobs = Job.objects.filter(id__in=job_ids)

    filter = request.GET.get("filter", None)

    if filter == 'Outstanding':
        jobs = jobs.filter(complete=False)
    elif filter == 'Complete':
        jobs = jobs.filter(complete=True)

    if jobs:
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    error = {'error': f"You have no {filter} jobs"}
    return Response(error)


# API to return a single Job
@api_view(['GET'])
def getJob(request, pk):
    try:
        job = Job.objects.get(id=pk)
        job_json = JobSerializer(job)
        return Response(job_json.data)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"})
    except Sample.DoesNotExist:
        return Response({"error": "Sample not found"})


# API to return all tests
@api_view(['GET'])
def getTests(request):
    tests = Test.objects.filter(user=request.user)

    if tests:
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

    error = {'error': 'You have no tests'}


# API to return a single test
@api_view(['GET'])
def getTest(request, pk):
    try:
        test = Test.objects.get(id=pk)
        test_json = TestSerializer(test)
        return Response(test_json.data)
    except Test.DoesNotExist:
        return Response({"error": "Test not found"})


