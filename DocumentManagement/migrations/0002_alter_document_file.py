# Generated by Django 4.0.2 on 2022-03-19 14:58

import backend.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DocumentManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(storage=backend.storage_backends.MediaStorage(), upload_to=models.CharField(max_length=30)),
        ),
    ]
