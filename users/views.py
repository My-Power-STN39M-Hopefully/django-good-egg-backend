from django.shortcuts import render
from .models import CustomUser
from good_egg.permissions import IsSelfOrAdmin
from .serializers import UserSerializer

# Create your views here.


class UserList(generics.ListCreateAPIView, ):
    queryset = CustomUser.objects.all()
    permission_classes = [IsSelfOrAdmin]
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsSelfOrAdmin]
    serializer_class = UserSerializer
