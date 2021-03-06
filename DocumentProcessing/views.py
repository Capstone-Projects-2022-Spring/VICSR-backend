from django.shortcuts import render
from requests import Response
import json
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import File, DocumentWord
from .serializers import FileSerializer
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from VocabularyManagement.models import StudySetWord, StudySet
from VocabularyManagement.serializers import StudySetWordSerializer


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
            'Delete': '/file/pk/delete',
            'Update': '/update/pk'
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
            return Response(status=status.HTTP_400_BAD_REQUEST, data=file.errors)

    @api_view(['GET'])
    def get_files(request):

        files = File.objects.filter(document__owner_id=request.user.id).order_by('document')
        print(files.count())
        print(files.values())

        if files:
            serializer = FileSerializer(files, many=True)
            return Response(serializer.data)
        else:
            data = {'File Count': files.count()}
            return Response(status=status.HTTP_404_NOT_FOUND, data=data)

    @api_view(['DELETE'])
    def delete_file(request, pk):
        file = get_object_or_404(File, pk=pk)
        file.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

    @api_view(['POST'])
    def update_highlight(request, pk):
        file = File.objects.get(id=pk)

        #extract all highlight here
        set = StudySet.objects.filter(generated_by=file.document).first()
        new_points = extract_points(request.data['highlight'], file.highlight)
        words = {}
        for i in new_points:
            for point in i['points']:
                #map out frequency of words
                word = DocumentWord.objects.filter(file=file, left__lte=point.get("x"), top__lte=point.get("y"),
                                                         right__gte=point.get("x"), bottom__gte=point.get("y"))
                if (word.count()!=0):
                    if (word.first() in words):
                        words[word.first()] +=1
                    else:
                        words[word.first()] = 1
            #iterate map, add to study set if over 5
            for key, value in words.items():
                if (value>5):
                    #check if word is already in studyset
                    if (StudySetWord.objects.filter(parent_set=set, word=key).count()==0):
                        StudySetWord.objects.create(owner_id=file.document.owner_id, parent_set=set, word=key.word,
                                                    translation="",
                                                    definition="")


        file.highlight = request.data['highlight']
        file.save(update_fields=['highlight'])
        data = StudySetWord.objects.filter(parent_set__generated_by=file.document)
        data2 = StudySetWordSerializer(data, many=True)
        del file
        del words
        return Response(data2.data)

def extract_points(newLines, oldLines):
    try:
        return ( eval(newLines)['lines'])[len(eval(oldLines)['lines']):]
    except:
        return eval(newLines)['lines']

