from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, serializers
from django import core
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


class BadApples(APIView):
    permission_classes = []
    # bad_apples = Incident.objects.filter(
    #     bad_apple=True).filter(officers__active=True).values('officers').annotate(total=Count('officers'))

    # print('!!!!!!!')
    # print('!!!!!!!')
    # print('!!!!!!!')
    # print('!!!!!!!')
    # print('!!!!!!!')
    # print('!!!!!!!')
    # print(bad_apples)
    # for i in bad_apples:
    #     bad_apples_map[i['officers']] = i['total']

    # officers = Officer.objects.filter(active=True)
    # print('!!!!!!!')
    # print('!!!!!!!')
    # print(bad_apples_map[1])
    # print(f'{officers[0]} {bad_apples_map}')

    # for o in officers:
    #     o.total = bad_apples_map[o].id
    serializer_class = OfficerSerializer

    def get(self, request):
        officers = Officer.objects.all()
        active_officers = []
        for officer in officers:
            if officer.active == True:
                active_officers.append(officer)
        print(active_officers)

        bad_apple_incidents = Incident.objects.filter(bad_apple=True)
        for incident in bad_apple_incidents:
            for officer_in_incident in incident.officers.all():
                if officer_in_incident in active_officers:
                    for officer in active_officers:
                        if officer.id in incident.officers.all():
                            if hasattr(officer, 'count'):
                                officer.count = officer.count + 1
                            else:
                                officer.count = 1
        data = core.serializers.serialize(
            'json', active_officers)
        return Response(data)


# Officer.objects.filter(
    # active = True).annotate(total = bad_apples_map[id])
