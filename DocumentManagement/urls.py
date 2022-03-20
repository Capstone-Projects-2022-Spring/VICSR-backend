from django.urls import path
from .views import DocumentView
from rest_framework.routers import SimpleRouter


urlpatterns = [
    # path('upload/', DocumentView.as_view(), name='upload'),
    path('', DocumentView.ApiOverview, name='docs'),
    path('add/', DocumentView.add_doc, name='add_doc'),
    path('list/', DocumentView.get_docs, name='get_docs'),
    path('delete/<int:pk>', DocumentView.delete_doc, name='delete_doc')
]
