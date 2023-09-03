from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Job(models.Model):
    job_number = models.CharField(max_length=50, unique=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Job No.: {self.job_number}"

    # Generate a unique job number
    @classmethod
    def create(cls):
        job_count = Job.objects.count() + 1
        current_year = datetime.now().year
        job_number = f"{current_year}-{job_count:04d}"
        job = cls(job_number=job_number)
        job.save()
        return job


class Sample(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="samples", blank=True, null=True
    )
    sample_id = models.CharField(max_length=50)
    batch = models.CharField(max_length=50)
    submitted = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    job = models.ForeignKey(
        Job, related_name="samples", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f"| Job: {self.job.job_number} \
                | Sample: {self.sample_id} \
                | Batch: {self.batch}"


class Attribute(models.Model):
    AMERICAN_FOULBROOD = "AFB"
    DIASTASE = "DIA"
    GLYPHOSATE = "GLY"
    LEPTOSPERIN = "LPS"
    TUTIN = "TUT"

    ATTRIBUTES = [
        (AMERICAN_FOULBROOD, "American Foulbrood"),
        (DIASTASE, "Diastase"),
        (GLYPHOSATE, "Glyphosate"),
        (LEPTOSPERIN, "Leptosperin"),
        (TUTIN, "Tutin"),
    ]

    name = models.CharField(
        max_length=3,
        choices=ATTRIBUTES,
        blank=False,
    )
    full_name = models.CharField(max_length=20, null=True, blank=True)
    units = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.get_name_display()}"

    # Create table of attributes
    @classmethod
    def create_table(cls):
        print("Creating attribute table")
        units = {
            "AFB": "cfu",
            "DIA": "schade",
            "GLY": "ppm",
            "LPS": "ppm",
            "TUT": "ppm",
        }
        for attr in Attribute.name.field.choices:
            attribute = cls(
                name=attr[0], full_name=attr[1], units=units[attr[0]])
            attribute.save()
        return


class Worklist(models.Model):
    worklist_number = models.CharField(max_length=50, unique=True)
    file = models.FileField(upload_to="worklists", blank=True, null=True)

    def __str__(self):
        return self.worklist_number

    @classmethod
    def create(cls):
        worklist_count = Worklist.objects.count() + 1
        worklist_number = f"wl-{worklist_count:04d}"
        worklist = cls(worklist_number=worklist_number)
        worklist.save()
        return worklist


class Test(models.Model):
    attribute = models.ForeignKey(
        Attribute, related_name="tests", on_delete=models.CASCADE
    )
    sample = models.ForeignKey(
        Sample, related_name="tests", on_delete=models.CASCADE)
    result = models.CharField(max_length=10, blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    worklist = models.ForeignKey(
        Worklist, related_name="tests", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"Sample: {self.sample.sample_id} \
                Test: {self.attribute.name}"
