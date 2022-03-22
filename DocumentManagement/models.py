from django.conf import settings
from django.db import models
from backend.storage_backends import MediaStorage


# Create your models here.

# Document management related models/functionality:
# Document list
# Document
# Deck List

class Document(models.Model):
    MODE_CHOICES = [
        ('TRL', 'Translation'),
        ('DEF', 'Definition')
    ]
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    filename = models.CharField(max_length=30)
    file = models.FileField(storage=MediaStorage())
    # size = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=3, choices=MODE_CHOICES)
    language = models.CharField(max_length=50)
    trans_language = models.CharField(max_length=50, blank=True)

    #saves file to user folder, and filename becomes folder for all files associated with document
    def save(self, *args, **kwargs):
        self.file.name = (str(self.owner_id) + "/" + self.filename + "/" + self.file.name)
        #second = Document(owner_id=self.owner_id, filename=self.filename, file=self.file,
                        #  date_added=self.date_added, mode=self.mode, language=self.language,
                       #   trans_language=self.trans_language)
        ####endless loop!!
       # second.file.name = (str(self.owner_id) + "/" + self.filename + "/" + "2")
        #print(second)
        #second.save()
        super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return self.filename

