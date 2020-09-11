from django.shortcuts import render
from .models import CustomUser
from good_egg.permissions import IsSelfOrAdmin
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


# Create your views here.


class UserList(generics.ListCreateAPIView, ):
    queryset = CustomUser.objects.all()
    permission_classes = [IsSelfOrAdmin]
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsSelfOrAdmin]
    serializer_class = UserSerializer


class RegistrationAPIView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # This method will return the serialized representations of new refresh
            #  and access tokens for the given user.
            refresh = RefreshToken.for_user(user)
            res = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
