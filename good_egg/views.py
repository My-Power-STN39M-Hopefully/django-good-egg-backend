from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, mixins, status
from .serializers import ForceSerializer, OfficerSerializer, UserSerializer, IncidentSerializer, UserSerializer
from django.contrib.auth.models import User
from .models import Force, Officer, Incident
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .permissions import IsAdminUserOrReadOnly, IsOwnerOrAdminOrReadOnly
User = get_user_model()


def landing_page(request):
    return render(request, 'landing_page.html')


class ForceList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Force.objects.all()
    serializer_class = ForceSerializer


class ForceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Force.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ForceSerializer


class OfficerList(generics.ListCreateAPIView, ):
    queryset = Officer.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OfficerSerializer


class OfficerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Officer.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OfficerSerializer


class UserList(generics.ListCreateAPIView, ):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer


class IncidentList(generics.ListCreateAPIView, ):
    queryset = Incident.objects.all()
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = IncidentSerializer


class IncidentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incident.objects.all()
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = IncidentSerializer


class RecentIncidents(generics.ListAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = IncidentSerializer
    last_two_weeks = timezone.now().date() - timedelta(days=14)
    queryset = Incident.objects.filter(date__gte=last_two_weeks)


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
