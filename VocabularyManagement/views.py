from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import StudySet, StudySetWord
from .serializers import StudySetSerializer, StudySetWordSerializer
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view


class StudySetView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    # basically returns the study set and study words list
    query_set = StudySet.objects.all()
    query_word = StudySetWord.objects.all()

    model_set = StudySet
    serializer_set = StudySetSerializer

    model_word = StudySetWord
    serializer_word = StudySetWordSerializer


    @api_view(['GET'])
    def ApiOverview(self, request):
        api_urls = {
            'Get Sets': '/sets/',
            'Get words by set': '/sets/pk',
            'Get all words': 'allWords/',
        }
        return Response(api_urls)

    @api_view(['GET'])
    def get_sets(request):

        study_sets = StudySet.objects.filter(owner_id=request.user.id)
        print(study_sets)

        if study_sets:
            serializer = StudySetSerializer(study_sets, many=True)
            return Response(serializer.data)
        else:
            data = {'Study Set': study_sets.count()}
            return Response(status=status.HTTP_404_NOT_FOUND, data=data)

    @api_view(['GET'])
    def get_words(request, pk):
        set_words = StudySetWord.objects.filter(parent_set_id=pk)

        if set_words:
            serializer = StudySetWordSerializer(set_words, many=True)
            return Response(serializer.data)
        else:
            data = {'Study Set Words': set_words.count()}
            return Response(status=status.HTTP_404_NOT_FOUND, data=data)

    @api_view(['GET'])
    def get_all_words(request):
        all_words = StudySetWord.objects.all()

        if all_words:
            serializer = StudySetWordSerializer(all_words, many=True)
            return Response(serializer.data)
        else:
            data = {'Study Set Words': all_words.count()}
            return Response(status=status.HTTP_404_NOT_FOUND, data=data)