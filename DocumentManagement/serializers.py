from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('owner_id', 'filename', 'file', 'size',
                  'date_added', 'mode', 'language', 'trans_language')
