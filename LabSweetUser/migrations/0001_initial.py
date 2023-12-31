# Generated by Django 4.2 on 2023-04-24 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sampleId', models.CharField(max_length=50)),
                ('sampleBatch', models.CharField(max_length=50)),
                ('submitted_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('complete', models.BooleanField(default=False)),
            ],
        ),
    ]
