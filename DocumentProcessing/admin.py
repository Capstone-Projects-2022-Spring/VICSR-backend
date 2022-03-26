from django.contrib import admin
from .models import File

# Register your models here.
class FileAdmin(admin.ModelAdmin):
    model = File
    list_display = ['document',  'file']

admin.site.register(File)
