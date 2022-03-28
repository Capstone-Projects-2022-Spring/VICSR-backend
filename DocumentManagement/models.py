from django.conf import settings
from django.db import models


class Document(models.Model):
    MODE_CHOICES = [
        ('TRL', 'Translation'),
        ('DEF', 'Definition')
    ]
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    filename = models.CharField(max_length=30)
    date_added = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=3, choices=MODE_CHOICES)
    language = models.CharField(max_length=50)
    trans_language = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.filename
