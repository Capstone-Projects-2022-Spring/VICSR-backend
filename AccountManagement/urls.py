from django.urls import path
from .views import AccountAPIView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', AccountAPIView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', AccountAPIView.as_view(), name='logout')
]
