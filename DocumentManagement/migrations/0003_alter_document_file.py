# Generated by Django 4.0.2 on 2022-03-19 17:04

import backend.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DocumentManagement', '0002_alter_document_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(storage=backend.storage_backends.MediaStorage(), upload_to=''),
        ),
    ]