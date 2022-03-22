from rest_framework import serializers
from .models import Document
from datetime import datetime


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'owner_id', 'filename', 'file',
                 'mode', 'language', 'trans_language')
        # fields = '__all__'
        #'date_added',
