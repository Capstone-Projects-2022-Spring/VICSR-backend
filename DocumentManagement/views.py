from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.conf import settings
from django.contrib.auth import get_user, get_user_model
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from rest_framework.decorators import api_view



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
            'Delete': '/delete/pk'
        }
        return Response(api_urls)

    @api_view(['POST'])
    def add_doc(request):

        request.data['owner_id'] = request.user.id
        doc = DocumentSerializer(data=request.data, context={'request': request})

        if doc.is_valid():
            doc.save()
            return Response(doc.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=doc.errors)

    @api_view(['GET'])
    def get_docs(request):

        docs = Document.objects.filter(owner_id=request.user.id)
        print(docs.count())
        print(docs.values())

        if docs:
            serializer = DocumentSerializer(docs, many=True)
            return Response(serializer.data)
        else:
            data = {'Document Count': docs.count()}
            return Response(status=status.HTTP_404_NOT_FOUND, data=data)

    @api_view(['DELETE'])
    def delete_doc(request, pk):
        doc = get_object_or_404(Document, pk=pk)
        if str(doc.owner_id) == str(request.user.id):
            doc.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
