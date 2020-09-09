from django.shortcuts import render, redirect
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from .serializers import ForceSerializer, OfficerSerializer, UserSerializer, IncidentSerializer
from django.contrib.auth.models import User
from .models import Force, Officer, Incident
from django.db.models import Q, Count


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
    permission_classes = [IsAuthenticated]
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


class GoodEggs(generics.ListCreateAPIView):

    good_eggs = Incident.objects.filter(
        bad_apple=False).filter(officers__active=True).values('officers').annotate(total=Count('officers')).order_by()

    queryset = good_eggs
    serializer_class = IncidentSerializer


class BadApples(generics.ListCreateAPIView):

    bad_apples = Incident.objects.filter(
        bad_apple=True).filter(officers__active=True).values('officers').annotate(total=Count('officers'))
    bad_apples_map = {}
    print('!!!!!!!')
    print('!!!!!!!')
    print('!!!!!!!')
    print('!!!!!!!')
    print('!!!!!!!')
    print('!!!!!!!')
    print(bad_apples)
    for i in bad_apples:
        bad_apples_map[i['officers']] = i['total']
    officers = Officer.objects.filter(active=True)
    print('!!!!!!!')
    print('!!!!!!!')
    print(officers)

    for o in officers:
        o.total = bad_apples_map[o.id]

    queryset = officers
    serializer_class = OfficerSerializer

# Officer.objects.filter(
    # active = True).annotate(total = bad_apples_map[id])
