from django.urls import path
from .views import FileView

urlpatterns = [
    path('', FileView.ApiOverview, name='files'),
    path('add/', FileView.add_file, name='add_file'),
    path('list/', FileView.get_files, name='get_files'),
    path('delete/<int:pk>', FileView.delete_file, name='delete_file'),
    path('patch/<int:pk>', FileView.update_file, name='update_file')
]
