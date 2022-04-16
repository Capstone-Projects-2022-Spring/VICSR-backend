# Generated by Django 4.0.2 on 2022-04-16 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VocabularyManagement', '0013_studysetword_owner_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='studysetword',
            name='ranking',
            field=models.IntegerField(choices=[(1, 'Easy'), (2, 'Medium'), (3, 'Hard')], default=2),
        ),
    ]
