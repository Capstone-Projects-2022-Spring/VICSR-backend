# Generated by Django 4.0.2 on 2022-03-26 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DocumentManagement', '0005_alter_file_document'),
    ]

    operations = [
        migrations.DeleteModel(
            name='File',
        ),
    ]
