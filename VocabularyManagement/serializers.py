from rest_framework import serializers
from .models import *

class StudySetSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySet
        fields = '__all__'


class StudySetWordSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudySetWord
        fields = '__all__'
