from django.urls import path
from .views import FileView

urlpatterns = [
    path('', FileView.ApiOverview, name='files'),
    path('add/', FileView.add_file, name='add_file'),
    path('list/', FileView.get_files, name='get_files'),
    path('delete/<int:pk>', FileView.delete_file, name='delete_file'),
    path('update/<int:pk>', FileView.update_highlight, name='update_highlight')
]
