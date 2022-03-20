from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


# Create your views here.
class DocumentView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
                              # SessionAuthentication)

    # need serializer and related functionality still (add, delete, rename, etc.)
    # need to also figure out how to just return specific users documents

    # basically returns the document list
    queryset = Document.objects.all()

    model = Document
    serializer_class = DocumentSerializer


"""
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_doc(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        docs = Document.objects.all()
        serializer = DocumentSerializer(docs)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, *args, **kwargs):
        Document.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

"""
