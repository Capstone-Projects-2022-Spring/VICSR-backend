# Generated by Django 4.0.2 on 2022-04-16 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VocabularyManagement', '0013_studysetword_owner_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='studysetword',
            name='ranking',
            field=models.IntegerField(default=2),
        ),
    ]