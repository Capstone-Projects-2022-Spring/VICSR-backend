from django.db import models
from django.contrib.auth.models import User
from DocumentManagement.models import Document
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from google.cloud import translate
import json
from googletrans import Translator
import os


def translate(text, target):
    import six
    from google.cloud import translate_v2 as translate
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file('google-credentials.json')
    # credentials = service_account.Credentials.from_service_account_info(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    translate_client = translate.Client(credentials=credentials)
    if isinstance(text, six.binary_type):
        text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)
    return result['translatedText']

# Create your models here.


class StudySet(models.Model):
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    generated_by = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    # date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class StudySetWord(models.Model):
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    parent_set = models.ForeignKey(StudySet, on_delete=models.CASCADE)
    word = models.CharField(max_length=65)
    translation = models.CharField(max_length=65, blank=True)
    definition = models.CharField(max_length=65, blank=True)

    def save(self, *args, **kwargs):
        set = StudySet.objects.get(id=self.parent_set.id)
        doc = Document.objects.get(id=set.generated_by.id)
        mode = doc.mode
        source_lang = doc.language
        target_lang = doc.trans_language

        if mode == 'TRL':
            # self.translation = translate_text(self.word, source_lang, target_lang)
            self.translation = translate(self.word, target_lang)

        super(StudySetWord, self).save(*args, **kwargs)

    def __str__(self):
        return self.word


@receiver(post_save, sender=Document)
def create_studySet(sender, instance, created, **kwargs):
    if created:
        StudySet.objects.create(owner_id=instance.owner_id, generated_by=instance, title=instance.filename)
