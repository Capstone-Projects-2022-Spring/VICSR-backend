# Generated by Django 4.0.2 on 2022-04-03 00:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('VocabularyManagement', '0012_remove_studysetword_owner_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='studysetword',
            name='owner_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
