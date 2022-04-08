from django.urls import path
from .views import StudySetView


urlpatterns = [
    path('sets/', StudySetView.get_sets, name='get_all_sets'),
    path('sets/fromDoc/<int:pk>', StudySetView.get_set_by_doc_id, name="get_set_by_doc_id"),
    path('sets/<int:pk>/words', StudySetView.get_words_by_set_id, name='get_words'),
    path('allWords', StudySetView.get_all_words, name='get_all_words'),
]