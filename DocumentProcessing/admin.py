from django.contrib import admin
from .models import File, DocumentWord

# Register your models here.
class FileAdmin(admin.ModelAdmin):
    model = File
    list_display = ['document',  'file', 'highlight']

admin.site.register(File)

class DocumentWordAdmin(admin.ModelAdmin):
    model = DocumentWord
    list_display = ['document', 'file', 'word',
                    'left', 'top', 'right', 'bottom']

admin.site.register(DocumentWord)
