import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from pdf2image import convert_from_bytes
from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

    def create(self, validated_data):
        f = validated_data['file']
        if (str(f)[-3:]=='pdf'):
            file = pdf_images(**validated_data)
        else:
            file = File.objects.create(**validated_data)
        return file


def pdf_images(document, file):
    name = str(file)[:-4]
    data = file.read()
    images = convert_from_bytes(data, fmt="png")
    for i, image in enumerate(images):
        f_name = name + str(i) + ".png"
        image_io = io.BytesIO()
        image.save(image_io, format="PNG")
        image_file = InMemoryUploadedFile(image_io, None, f_name, 'image/png',
                                          image_io.tell(), None)
        file = File.objects.create(document=document, file=image_file)
        file.save()
    return file

