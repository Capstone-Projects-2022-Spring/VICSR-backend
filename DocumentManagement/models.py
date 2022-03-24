from django.conf import settings
from django.db import models
from backend.storage_backends import MediaStorage
from pdf2image import convert_from_path, convert_from_bytes
import io

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
        orig_name = self.file.name
        if (self.file.name[-3:]=='pdf'):

            ###Does not work proprely right now
            images = convert_from_bytes(self.file.read(), poppler_path=r'C:\Program Files\poppler-0.68.0\bin', fmt="png")
            for i, image in enumerate(images):
                fname=orig_name[:-4] + str(i) + ".png"
                print(fname)
                print(image)
                #save file locally
                #image.save(fname)

                ##trying to store file as in variable rather than local filesystem
                buffer = io.BytesIO()
                #image.save(buffer, "PNG")
                #self.file.save(fname, image)

                ##issues trying to figure out how to save a local var or update
                doc = Document(owner_id=self.owner_id, filename=self.file.name, file=buffer,
                               mode=self.mode, language=self.language,
                               trans_language=self.trans_language)
                self.file.name = (str(self.owner_id) + "/" + self.filename + "/" + self.file.name)
                doc.save()
        else:
            self.file.name = (str(self.owner_id) + "/" + self.filename + "/" + self.file.name)
            super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return self.filename

