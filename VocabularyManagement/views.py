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
            'Get set by doc id': 'sets/fromDoc/pk',
            'Get words by set': '/sets/fromDoc/pk/words',
            'Get all words': 'allWords/',
            'Update ranking': 'sets/word/update/pk',
            'Delete set': 'sets/delete/pk'
            'Update name': 'sets/update/pk',
        }
        return Response(api_urls)

    @api_view(['GET'])
    def get_sets(request):

        study_sets = StudySet.objects.filter(owner_id=request.user.id)

        if study_sets:
            serializer = StudySetSerializer(study_sets, many=True)
            return Response(serializer.data)
        else:
            data = {'Study Set': study_sets.count()}
            return Response(status=status.HTTP_404_NOT_FOUND, data=data)

    @api_view(['GET'])
    def get_set_by_doc_id(request, pk):
        set = StudySet.objects.filter(generated_by_id=pk, owner_id=request.user.id)

        if set:
            serializer = StudySetSerializer(set, many=True)
            return Response(serializer.data)
        else:
            data = {'Study Set Words': set.count()}
            return Response(status=status.HTTP_404_NOT_FOUND, data=data)

    @api_view(['GET'])
    def get_words_by_set_id(request, pk):
        set_words = StudySetWord.objects.filter(parent_set_id=pk, owner_id=request.user.id).order_by('-ranking')

        if set_words:
            serializer = StudySetWordSerializer(set_words, many=True)
            return Response(serializer.data)
        else:
            data = {'Study Set Words': set_words.count()}
            return Response(status=status.HTTP_404_NOT_FOUND, data=data)

    @api_view(['GET'])
    def get_all_words(request):
        all_words = StudySetWord.objects.filter(owner_id=request.user.id)

        if all_words:
            serializer = StudySetWordSerializer(all_words, many=True)
            return Response(serializer.data)
        else:
            data = {'Study Set Words': all_words.count()}
            return Response(status=status.HTTP_404_NOT_FOUND, data=data)

    @api_view(['POST'])
    def update_ranking(request, pk):
        word = StudySetWord.objects.get(id=pk)
        word.ranking = request.data['ranking']
        word.save(update_fields=['ranking'])
        return Response(word.ranking)

    @api_view(['DELETE'])
    def delete_set(request, pk):
        studySet = get_object_or_404(StudySet, pk=pk)

        if str(studySet.owner_id_id) == str(request.user.id) and studySet.generated_by is None:
            studySet.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @api_view(['POST'])
    def update_name(request, pk):

        studySet = StudySet.objects.get(id=pk)
        studySet.title = request.data['title']

        studySet.save(update_fields=['title'])
        return Response(studySet.title)

