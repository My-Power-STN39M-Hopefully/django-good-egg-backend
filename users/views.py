from django.shortcuts import render
from .models import CustomUser
from good_egg.permissions import IsSelfOrAdmin, PostWithoutAuth
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import permissions

class UserList(generics.ListCreateAPIView ):
    queryset = CustomUser.objects.all()
    permission_classes = [PostWithoutAuth | permissions.IsAdminUser]
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [ IsSelfOrAdmin ]
    serializer_class = UserSerializer