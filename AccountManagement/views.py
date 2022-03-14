"""

from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.generics import CreateAPIView
from .serializers import AccountSerializer
from rest_framework.response import Response
from rest_framework import status

"""

"""

# Create your views here.
class AccountAPIView(CreateAPIView):
    serializer_class = AccountSerializer
    queryset = get_user_model().objects.all()

    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # create authentication token

        return Response(
            {**serializer.data},
            # {**serializer.data, **token data}
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def logout(self, request, format=None):
        # delete user token, something like: request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

"""