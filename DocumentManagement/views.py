from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError

from .models import Document
from .serializers import DocumentSerializer

try:
    from PIL import Image  # PIL is the pillow
except ImportError:
    import Image
import pytesseract
from pytesseract import Output
import numpy as np
import cv2
# import IMG


# convert file to images
def convert_to_images(file):

    images = convert_from_path(file)

    for i, image in enumerate(images):
        name = "page" + str(i) + ".png"
        image.save(name, "PNG")  # find a way to save to s3 instead of locally


# Create your views here.
class DocumentView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
                              # SessionAuthentication)

    # basically returns the document list
    queryset = Document.objects.all()

    model = Document
    serializer_class = DocumentSerializer

    @api_view(['GET'])
    def ApiOverview(self, request):
        api_urls = {
            'all_docs': '/',
            'Add': '/add',
            'Delete': '/doc/delete/pk'
        }
        return Response(api_urls)

    @api_view(['POST'])
    def add_doc(request):
        doc = DocumentSerializer(data=request.data)
        if doc.is_valid():
            doc.save()
            return Response(doc.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    def get_docs(request):

        print(request.user.id)

        docs = Document.objects.filter(owner_id=request.user.id)
        print(docs.count())

        if docs:
            serializer = DocumentSerializer(docs, many=True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @api_view(['DELETE'])
    def delete_doc(request, pk):
        doc = get_object_or_404(Document, pk=pk)
        doc.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
