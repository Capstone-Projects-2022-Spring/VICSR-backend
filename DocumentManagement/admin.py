from django.contrib import admin
from .models import Document, File


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    list_display = ['owner_id', 'filename', 'files'
                     'mode', 'language', 'trans_language']

class FileAdmin(admin.ModelAdmin):
    model = File
    list_display = ['document',  'file']


# Register your models here.
admin.site.register(Document)
admin.site.register(File)

#'date_added',


