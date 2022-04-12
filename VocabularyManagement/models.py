import random

from django.db import models
from django.contrib.auth.models import User
from DocumentManagement.models import Document
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from google.cloud import translate
import json
import os
import wikipedia
import wikipediaapi

# with open('google-credentials.json') as file:
#    data = json.load(file)
#    print(data)

# the json credentials stored as env variable
json_str = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')


def translate_text(text, source_lang, target_lang):

    client = translate.TranslationServiceClient.from_service_account_json(os.environ.get('GOOGLE_CREDENTIALS'))
    parent = client.location_path(os.environ.get('GOOGLE_PROJECT_ID'), "global")

    # client = translate.TranslationServiceClient.from_service_account_json('google-credentials.json')
    # parent = client.location_path(data['project_id'], "global")
    response = client.get_supported_languages(parent, 'en')
    languages = response.languages

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code=source_lang,
        target_language_code=target_lang
    )
    for translation in response.translations:
        translation = translation.translated_text
        # print(translation.translated_text)
    return translation


def get_definition(word, lang):
    wikipedia.set_lang(lang)
    try:
        definition = wikipedia.page(word).summary[0:65]
    except wikipedia.exceptions.DisambiguationError as d:
        print(d.options[0])
        definition = wikipedia.page(d.options[0]).summary[0:65]
    except wikipedia.exceptions.PageError as p:
        definition = wikipedia.page(wikipedia.suggest(word)).summary[0:65]
    return definition

# Create your models here.

#Vocabulary Management related models/functionality:
#Vocabulary
#Study Set


#Started study set - will expand on in future sprints
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
            self.translation = translate_text(self.word, source_lang, target_lang)
        if mode == 'DEF':
            self.definition = get_definition(self.word, source_lang)

        super(StudySetWord, self).save(*args, **kwargs)

    def __str__(self):
        return self.word


@receiver(post_save, sender=Document)
def create_studySet(sender, instance, created, **kwargs):
    if created:
        StudySet.objects.create(owner_id=instance.owner_id, generated_by=instance, title=instance.filename)
