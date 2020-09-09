from django.shortcuts import render, redirect
from rest_framework import generics, permissions, mixins
from .serializers import ForceSerializer, OfficerSerializer
from .models import Force, Officer

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
