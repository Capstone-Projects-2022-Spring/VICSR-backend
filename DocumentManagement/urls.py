from django.urls import path
from .views import DocumentView
from rest_framework.routers import SimpleRouter


urlpatterns = [
    # path('upload/', DocumentView.as_view(), name='upload'),
]
