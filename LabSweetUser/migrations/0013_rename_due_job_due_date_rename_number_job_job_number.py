# Generated by Django 4.2 on 2023-05-27 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LabSweetUser', '0012_remove_attribute_abbreviated_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='due',
            new_name='due_date',
        ),
        migrations.RenameField(
            model_name='job',
            old_name='number',
            new_name='job_number',
        ),
    ]
