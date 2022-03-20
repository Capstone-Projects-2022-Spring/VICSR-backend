from django.contrib import admin
from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    list_display = ['owner_id', 'filename', 'file',
                    'date_added', 'mode', 'language', 'trans_language']


# Register your models here.
admin.site.register(Document)


