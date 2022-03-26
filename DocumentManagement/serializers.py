from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from .models import Document
from DocumentProcessing.serializers import FileSerializer
from DocumentProcessing.models import File
from pdf2image import convert_from_bytes
import io


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
            if (str(file)[-3:]=='pdf'):
               pdf_images(document, file)
            else:
                File.objects.create(document=document, file=file)
        return document

def pdf_images(document, file):
    name = str(file)[:-4]
    data = file.read()
    images = convert_from_bytes(data, poppler_path=r'C:\Program Files\poppler-0.68.0\bin', fmt="png")
    for i, image in enumerate(images):
        f_name = name + str(i) + ".png"
        image_io = io.BytesIO()
        image.save(image_io, format="PNG")
        image_file = InMemoryUploadedFile(image_io, None, f_name, 'image/png',
                                          image_io.tell(), None)
        File.objects.create(document=document, file=image_file)


