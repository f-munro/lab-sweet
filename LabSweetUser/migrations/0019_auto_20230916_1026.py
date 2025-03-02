# Generated by Django 4.2 on 2023-09-16 10:26

from django.db import migrations

# Populates the attribute table with the attribute choices.
def populate_attribute_table(apps, schema_editor):
    Attribute = apps.get_model("LabSweetUser", "Attribute")
    units = {
            "AFB": "cfu",
            "DIA": "schade",
            "GLY": "ppm",
            "UMF": "UMF",
            "TUT": "ppm",
        }
    for attr in Attribute.name.field.choices:
        attribute = Attribute.objects.create(
            name=attr[0],
            full_name=attr[1],
            units=units[attr[0]]
        )


class Migration(migrations.Migration):

    dependencies = [
        ('LabSweetUser', '0018_remove_job_due_date'),
    ]

    operations = [
        migrations.RunPython(populate_attribute_table),
    ]
