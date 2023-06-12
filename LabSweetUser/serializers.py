from rest_framework import serializers
from .models import Job, Test, Sample, Attribute


class SampleSerializer(serializers.ModelSerializer):
    submitted = serializers.SerializerMethodField()
    attribute_name = serializers.SerializerMethodField()
    '''
    def get_attribute_name(self, obj):
        return [test.attribute.get_name_display() for test in obj.tests.all()]
    '''

    def get_attribute_name(self, obj):
        return [test.attribute.get_name_display() for test in obj.tests.all()]

    def get_submitted(self, obj):
        return obj.submitted.strftime("%d %b %Y")

    class Meta:
        model = Sample
        fields = ['id', 'user', 'sample_id', 'batch',
                  'submitted', 'complete', 'job', 'tests', 'attribute_name']
        depth = 2


class JobSerializer(serializers.ModelSerializer):
    due_date = serializers.SerializerMethodField()

    def get_due_date(self, obj):
        return obj.due_date.strftime("%d %b %Y")

    class Meta:
        model = Job
        fields = ['id', 'job_number', 'due_date', 'complete', 'samples']
        depth = 3


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='get_name_display')

    class Meta:
        model = Attribute
        fields = ['get_name_display', 'units']
