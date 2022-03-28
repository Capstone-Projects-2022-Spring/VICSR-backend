from io import BytesIO

import numpy
from django.core.files.uploadedfile import InMemoryUploadedFile

try:
    from PIL import Image  # PIL is the pillow
except ImportError:
    import Image
from django.conf import settings
from django.db import models
from backend.storage_backends import MediaStorage
from DocumentManagement.models import Document
from .process import main as process
import cv2

# Create your models here.


#ocumentProcessing related models/functionality:
#Document Preprocessing
    #List of words in Doc
#Highlight exraction

class File(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(storage=MediaStorage())

    def save(self, *args, **kwargs):
        ##open file as PIL Image and send for processing
        pil_image_obj = Image.open(self.file.file)
        new = process(pil_image_obj)
        ##after processed save as file and replace file in model
        image_io = BytesIO()
        new.save(image_io, format="PNG")
        image_file = InMemoryUploadedFile(image_io, None, self.file.name, 'image/png',
                                          image_io.tell(), None)
        self.file = image_file
        self.file.name = (str(self.document.owner_id) + "/" + self.document.filename + "/" + self.file.name)
        super(File, self).save(*args, **kwargs)

    def __str__(self):
        return self.file.name



""" commenting out -- not relevant for milestone 1 and may need reworking 
leaving as starting point when returning


class DocumentWords(models.Model):
    generated_by = models.ForeignKey(Document, on_delete=models.CASCADE)
    word = models.CharField(max_length=65)
    ##coordinates from tesseract - may want to change
    left = models.IntegerField()
    top = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    """
