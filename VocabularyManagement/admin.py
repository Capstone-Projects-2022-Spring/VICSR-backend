from django.contrib import admin
from .models import *

# Register your models here.
class StudySetAdmin(admin.ModelAdmin):
    model = StudySet
    list_display = ['owner_id', 'generated_by', 'title',
                    'date_added']


# Register your models here.
admin.site.register(StudySet)


class StudySetWordAdmin(admin.ModelAdmin):
    model = StudySetWord
    list_display = ['parent_set', 'word', 'definition',
                    'translation']


# Register your models here.
admin.site.register(StudySetWord)
