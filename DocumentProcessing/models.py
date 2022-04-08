from io import BytesIO
import numpy
import cv2
import string
import pytesseract
from django.core.files.uploadedfile import InMemoryUploadedFile
from pytesseract import Output
import time

try:
    from PIL import Image  # PIL is the pillow
except ImportError:
    import Image
from django.db import models
from backend.storage_backends import MediaStorage
from DocumentManagement.models import Document
from VocabularyManagement.models import StudySet, StudySetWord
from .process import preprocess, check_highlight_amount
from django.db.models.signals import post_save
from django.dispatch import receiver


def get_words(image, document, file):
    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    # remove highlight for OCR extraction
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray_img = img_hsv[:, :, 2]
    out_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 22)

    set = StudySet.objects.filter(generated_by=document).first()
    # check if study set exists or not -- if not create it
    if (not set):
        set = StudySet.objects.create(owner_id=document.owner_id, generated_by=document, title=document.filename)

    # extract and add to database
    d = pytesseract.image_to_data(out_img, output_type=Output.DICT)
    n_boxes = len(d['text'])
    bulkList = []
    for i in range(n_boxes):
        if int(float(d['conf'][i])) > 60:
            word = (d['text'][i]).translate(str.maketrans('', '', string.punctuation))
            #word_query = StudySetWord.objects.filter(parent_set=set, word=word)
            bulkList.append(DocumentWord(document=document, file=file, word=word, left=d['left'][i], top=d['top'][i],
                                         right=d['width'][i]+d['left'][i], bottom=d['height'][i]+d['top'][i]))
            # DocumentWord.objects.create(document=document, file=file, word=word,
            #                              left=d['left'][i], top=d['top'][i],
            #                              width=d['width'][i], height=d['height'][i])
            #if len(word_query) == 0:
            amount = check_highlight_amount(image, (word, (d['left'][i], d['top'][i], d['width'][i], d['height'][i])))
            if (amount>=50.0):
                w = StudySetWord.objects.create(owner_id=document.owner_id, parent_set=set, word=word, translation="", definition="")
    DocumentWord.objects.bulk_create(bulkList)


class File(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(storage=MediaStorage())

    def save(self, *args, **kwargs):
        timestart = time.time()
        # open file as PIL Image and send for processing
        pil_image_obj = Image.open(self.file.file)
        new = preprocess(pil_image_obj)

        # after processed save as file and replace file in model
        image_io = BytesIO()
        new.save(image_io, format="PNG")
        image_file = InMemoryUploadedFile(image_io, None, self.file.name, 'image/png',
                                          image_io.tell(), None)
        self.file = image_file
        print("Preprocess (and save) one file time: " + str(time.time() - timestart))
        self.file.name = (str(self.document.owner_id) + "/" + self.document.filename + "/" + self.file.name)
        super(File, self).save(*args, **kwargs)

        # process OCR and add words to DB
        time_ocr = time.time()
        get_words(new, self.document, self)
        print("time for OCR + Studyset Create: " + str(time.time() - time_ocr))
        #print("time from start to end OCR for " + self.file.name + ": " + str(time.time() - timestart))

    def __str__(self):
        return self.file.name


class DocumentWord(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    word = models.CharField(max_length=65)
    left = models.IntegerField()
    top = models.IntegerField()
    right = models.IntegerField()
    bottom = models.IntegerField()
    #right = left+width
    #bottom = top-height

   # def right(self):
    #    return self.left + self.width

    #def bottom(self):
     #   return self.top - self.height

    def __str__(self):
        return self.word

"""
@receiver(post_save, sender=File)
def create_another(sender, instance, created, **kwargs):
    if created:
        print("IN CREATED - SIGNAL")
        print(instance)
        print(sender)
        pil_image_obj = Image.open(instance.file)
        image_io = BytesIO()
        pil_image_obj.save(image_io, format="PNG")
        time_ocr = time.time()
        get_words(pil_image_obj, instance.document, instance)
        print("time for OCR : " + instance.file.name + str(time.time() - time_ocr))"""


"""
class File(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(storage=MediaStorage())

    def save(self, *args, **kwargs):
        # open file as PIL Image
        timestart = time.time()
        pil_image_obj = Image.open(self.file.file)
        if (self.pk):
            image_io = BytesIO()
            pil_image_obj.save(image_io, format="PNG")
        else:
            # send for processing
            pil_image_obj = preprocess(pil_image_obj)
            print("Preprocess one file time: " + str(time.time() - timestart))

            # after processed save as file and replace file in model
            image_io = BytesIO()
            pil_image_obj.save(image_io, format="PNG")
            image_file = InMemoryUploadedFile(image_io, None, self.file.name, 'image/png',
                                              image_io.tell(), None)
            self.file = image_file

        self.file.name = (str(self.document.owner_id) + "/" + self.document.filename + "/" + self.file.name)
        super(File, self).save(*args, **kwargs)

        # process OCR and add words to DB
        time_ocr = time.time()
        get_words(pil_image_obj, self.document, self)
        print("time for OCR: " + str(time.time() - time_ocr))
        print("time from start to end OCR for " + self.file.name + ": " + str(time.time() - timestart))

    def __str__(self):
        return self.file.name

"""
