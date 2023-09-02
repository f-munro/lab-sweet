from rest_framework import serializers
from .models import Job, Sample, Test, Worklist


class SampleSerializer(serializers.ModelSerializer):
    submitted = serializers.SerializerMethodField()
    attribute_name = serializers.SerializerMethodField()

    def get_attribute_name(self, obj):
        return [test.attribute.get_name_display() for test in obj.tests.all()]

    def get_submitted(self, obj):
        return obj.submitted.strftime("%d %b %Y")

    class Meta:
        model = Sample
        fields = [
            'id', 'user', 'sample_id', 'batch',
            'submitted', 'complete', 'job', 'tests', 'attribute_name'
        ]
        depth = 2


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ['id', 'job_number', 'complete', 'samples']
        depth = 3


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'attribute', 'sample', 'result', 'worklist']
        depth = 2


class WorklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worklist
        fields = ['worklist_number', 'tests']
        depth = 3
