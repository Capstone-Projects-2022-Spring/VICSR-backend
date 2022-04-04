from django.db import models
from django.contrib.auth.models import User
from DocumentManagement.models import Document
from django.conf import settings



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

    def __str__(self):
        return self.word



