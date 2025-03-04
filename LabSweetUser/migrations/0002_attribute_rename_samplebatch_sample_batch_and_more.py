# Generated by Django 4.2 on 2023-04-25 03:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LabSweetUser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('AFB', 'American Foulbrood'), ('DIA', 'Diastase'), ('GLY', 'Glyphosate'), ('UMF', 'UMF'), ('TUT', 'Tutin')], max_length=3)),
                ('abbreviated_name', models.CharField(max_length=10)),
                ('units', models.CharField(max_length=6)),
            ],
        ),
        migrations.RenameField(
            model_name='sample',
            old_name='sampleBatch',
            new_name='batch',
        ),
        migrations.RenameField(
            model_name='sample',
            old_name='sampleId',
            new_name='sample_id',
        ),
        migrations.RenameField(
            model_name='sample',
            old_name='submitted_on',
            new_name='submitted',
        ),
        migrations.RenameField(
            model_name='sample',
            old_name='updated_on',
            new_name='updated',
        ),
        migrations.AddField(
            model_name='sample',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='samples', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=10)),
                ('completed', models.DateTimeField(auto_now_add=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='LabSweetUser.attribute')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='LabSweetUser.sample')),
            ],
        ),
    ]
