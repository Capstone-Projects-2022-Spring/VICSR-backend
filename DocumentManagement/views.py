from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView


# Create your views here.
class DocumentView(APIView):

    # need serializer and related functionality still (add, delete, rename, etc.)
    # need to also figure out how to just return specific users documents

    serializer_class = DocumentSerializer

    # basically returns the document list
    queryset = Document.objects.all()

    parser_classes = (MultiPartParser, FormParser)

    def upload(self, request, *args, **kwargs):
        document_serializer = DocumentSerializer(data=request.data)
        if document_serializer.is_valid():
            document_serializer.save()
            return Response(document_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(document_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        document = Document.objects.get(pk)
        document.file.delete(save=True)
