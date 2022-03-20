from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'owner_id', 'filename', 'file',
                 'date_added', 'mode', 'language', 'trans_language')
        # fields = '__all__'
