from django.urls import path
from .views import StudySetView


urlpatterns = [
    path('sets/', StudySetView.get_sets, name='get_sets'),
    path('sets/<int:pk>', StudySetView.get_words, name='get_words'),
    path('allWords', StudySetView.get_all_words, name='get_all_words'),
]
