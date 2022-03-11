from django.db import models

# Create your models here.


#ocumentProcessing related models/functionality:
#Document Preprocessing
    #List of words in Doc
#Highlight exraction


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
