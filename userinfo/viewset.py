#!/usr/bin/env python

from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import *
from rest_framework.response import Response
from .permissions import *

class UserListViewSet(generics.ListAPIView):
    """
    get:
        Get all the Users available in the system - Admin Only
    """
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    permission_classes = (IsAuthenticated, IsAdminUser, )

class UserCreateViewSet(generics.CreateAPIView):
    """
    post:
        Register a user.
        Fields required - `username`, `email`, `password`
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

class UserDetailViewSet(generics.ListAPIView):
    """
    get:
        Get a specific user information when logged In
    """
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    permission_classes = (IsAuthenticated, IsOwnerOnly, )

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if request.user:
            user = User.objects.filter(username=request.user).get()
            serializer = UserGetSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
