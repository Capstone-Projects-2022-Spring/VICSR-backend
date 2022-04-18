from django.urls import path
from .views import StudySetView


urlpatterns = [
    path('sets/', StudySetView.get_sets, name='get_all_sets'),
    path('sets/fromDoc/<int:pk>', StudySetView.get_set_by_doc_id, name="get_set_by_doc_id"),
    path('sets/<int:pk>/words', StudySetView.get_words_by_set_id, name='get_words'),
    path('allWords', StudySetView.get_all_words, name='get_all_words'),
    path('sets/words/update/<int:pk>', StudySetView.update_ranking, name='update_ranking'),
    path('sets/delete/<int:pk>', StudySetView.delete_set, name='delete_set'),
    path('sets/update/<int:pk>', StudySetView.update_name, name='update_name'),
    path('sets/add', StudySetView.new_set, name='new_set'),
    path('sets/addWord', StudySetView.add_word_to_set, name='add_word_to_set')
]
