from django.shortcuts import render
from requests import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import File
from .serializers import FileSerializer
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view


class FileView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    # SessionAuthentication)

    # basically returns the document list
    queryset = File.objects.all()

    model = File
    serializer_class = FileSerializer

    @api_view(['GET'])
    def ApiOverview(self, request):
        api_urls = {
            'all_files': '/',
            'Add': '/add',
            'Delete': '/file/pk/delete'
        }
        return Response(api_urls)

    @api_view(['POST'])
    def add_file(request):

        #request.data['owner_id'] = request.user.id
        file = FileSerializer(data=request.data)

        if file.is_valid():
            file.save()
            return Response(file.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    def get_files(request):

        files = File.objects.filter(document__owner_id=request.user.id).order_by('document')
        print(files.count())
        print(files.values())

        if files:
            serializer = FileSerializer(files, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @api_view(['DELETE'])
    def delete_file(request, pk):
        file = get_object_or_404(File, pk=pk)
        file.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

