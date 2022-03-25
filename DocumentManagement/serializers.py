from rest_framework import serializers
from .models import Document, File
import json
from datetime import datetime

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, required=False)
    class Meta:
        model = Document
        fields = ('id', 'owner_id', 'filename', 'files',
                'mode', 'language', 'trans_language')
        #fields = '__all__'
        #'date_added',

    def create(self, validated_data):
        files = self.context['request'].FILES
        document = Document.objects.create(**validated_data)
        for file in files.values():
            File.objects.create(document=document, file=file)
        return document
