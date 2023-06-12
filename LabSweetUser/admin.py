from django.contrib import admin

# Register your models here.

from .models import Sample, Test, Attribute, Job


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ('job', 'sample_id', 'batch', 'test_count',
                    'submitted', 'complete', 'user')
    list_filter = ('user', 'batch')
    readonly_fields = ['submitted']

    @admin.display(description='No. of Tests')
    def test_count(self, obj):
        return obj.tests.count()


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_number', 'due_date', 'complete')
    '''
    @admin.display(description='Total Tests')
    def test_count(self, obj):
        return obj.samples.count()

    @admin.display(description='No. of Samples')
    def sample_count(self, obj):
        return obj.tests.values('sample').distinct().count()

    @admin.display(description='Outstanding Tests')
    def outstanding(self, obj):
        return obj.tests.filter(completed=False).count()
    '''


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('sample', 'attribute', 'result', 'units')

    @admin.display(description='Units')
    def units(self, obj):
        return obj.attribute.units


admin.site.register(Attribute)
