from django.shortcuts import render, redirect
from rest_framework import generics, permissions, mixins
from .serializers import ForceSerializer, OfficerSerializer, UserSerializer, IncidentSerializer
from django.contrib.auth.models import User
from .models import Force, Officer, Incident

def landing_page(request):
    return render(request, 'landing_page.html')


class ForceList(generics.ListCreateAPIView, ):
    queryset = Force.objects.all()
    serializer_class = ForceSerializer

class ForceDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Force.objects.all()
  serializer_class = ForceSerializer

class OfficerList(generics.ListCreateAPIView, ):
    queryset = Officer.objects.all()
    serializer_class = OfficerSerializer


class OfficerDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Officer.objects.all()
  serializer_class = OfficerSerializer


class UserList(generics.ListCreateAPIView, ):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer


class IncidentList(generics.ListCreateAPIView, ):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer


class IncidentDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Incident.objects.all()
  serializer_class = IncidentSerializer
