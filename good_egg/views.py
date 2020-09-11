from jsonview.decorators import json_view
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, mixins, serializers
from django import core
from rest_framework.permissions import IsAuthenticated
from .serializers import ForceSerializer, OfficerSerializer, IncidentSerializer, PersonSerializer
from django.contrib.auth.models import User
from .models import Force, Officer, Incident, Person
from django.db.models import Q, Count
from django.forms.models import model_to_dict
from jsonview.views import JsonView
import copy
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions, mixins, status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .permissions import IsAdminUserOrReadOnly, IsOwnerOrAdminOrReadOnly, IsSelfOrAdmin
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


class PersonList(generics.ListCreateAPIView, ):
    queryset = Person.objects.all()
    permission_classes = [IsSelfOrAdmin]
    serializer_class = PersonSerializer


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    permission_classes = [IsSelfOrAdmin]
    serializer_class = PersonSerializer


class OfficerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Officer.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OfficerSerializer


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


class OfficerList(generics.ListCreateAPIView, ):
    queryset = Officer.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OfficerSerializer


class OfficerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Officer.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OfficerSerializer

# This Json view will return two items within a dictionary
#   1. Under the key bad_apples it will show a list of active officers with a 'count' property. That count is the number of times someone has created a "bad apple" incident with them
#   2. Under the key good_eggs it will show a list of active officers with a 'count' property. That count is the number of times someone has created a "good egg" incident with them
#
# This is done in two parts.
#   Step 1: Find the number of times a officer is reported being a "good egg" or a "bad apple"
#       1. Create two sets of dictionaries: bad_apple_officer_count_by_id, good_egg_officer_count_by_id these will store
#          the id of the officer and the number of times they have been reported being a "good egg" or a "bad apple"
#       2. Loop over all incidents and get the list of active officers
#       3. If the incident is a "bad apple" incident (incident.bad_apple == True)
#           1. Check if active officer id exists in bad_apple_officer_count_by_id
#           2. If yes then get the number of incidents recorded using the active officer id and add 1 to it
#           3. If no then add the officer id to bad_apple_officer_count_by_id with a value of 1
#       4. If the incident is a "good egg" incident (incident.bad_apple == False)
#           1. Check if active officer id exists in good_egg_officer_count_by_id
#           2. If yes then get the number of incidents recorded using the active officer id and add 1 to it
#           3. If no then add the officer id to good_egg_officer_count_by_id with a value of 1
#    Step 2: Add the "good egg" and "bad apple" incident count to the list of active officers
#           1. Loop over the list of active officers
#           2. If the officer id is present in bad_apple_officer_count_by_id add that value to the officer as "count",
#              if not present set it to zero
#           3. Add officer to the list "bad_apples"
#           4. If the officer id is present in good_egg_officer_count_by_id add that value to the officer as "count",
#              if not present set it to zero
#           5. Add officer to the list of "good_eggs"
#           6. Return both "good_egg" and "bad_apple" lists ordered with the officer with the highest number of incidents
#              is shown first.


class GoodEggsBadApples(JsonView):
    def get_context_data(self, **kwargs):
        # Create empty dicts for the good eggs and badd apple counts
        # Key will be  officer id
        bad_apple_officer_count_by_id = {}
        good_egg_officer_count_by_id = {}

        # Step one:
        # Loop over all incidents
        for incident in Incident.objects.all():
            # Loop over active officers involved in  a incident
            for officer_in_incident in incident.officers.filter(active=True):
                # For bad apple incidents
                if(incident.bad_apple == True):
                    # If officer id exists in bad_apple_officer_count_by_id
                    if(officer_in_incident.id in bad_apple_officer_count_by_id):
                        # Get the current incident count
                        count = bad_apple_officer_count_by_id[officer_in_incident.id]
                        # Increase the count of the bad apple incidents
                        bad_apple_officer_count_by_id[officer_in_incident.id] = count+1
                    else:
                        # Create a new key in bad_apple_officer_count_by_id for the new id
                        bad_apple_officer_count_by_id[officer_in_incident.id] = 1
                # For good egg incidents
                else:
                    # If officer id exists in good_egg_officer_count_by_id
                    if(officer_in_incident.id in good_egg_officer_count_by_id):
                        # Get the current incident count
                        count = good_egg_officer_count_by_id[officer_in_incident.id]
                        # Increase the count of the good egg incidents
                        good_egg_officer_count_by_id[officer_in_incident.id] = count+1
                    else:
                        # Create a new key in good_egg_officer_count_by_id for the new id
                        good_egg_officer_count_by_id[officer_in_incident.id] = 1

        # Step two:
        # Create two new lists
        bad_apples = []
        good_eggs = []
        # Loop over the list of active officers
        for active_officer in Officer.objects.filter(active=True).all():
            # Convert the officer model to a dictionary
            # NOTE if this is not done you WILL NOT be able to add new fields to the object
            active_officer_dict = model_to_dict(active_officer)

            # If the id of the officer is found with in bad_apple_officer_count_by_id
            if active_officer_dict['id'] in bad_apple_officer_count_by_id:
                # Set the officers incident count to the calculated value
                active_officer_dict['count'] = bad_apple_officer_count_by_id[active_officer_dict['id']]
            else:
                # Otherwise set the count to zero
                active_officer_dict['count'] = 0

            # Add officer to the list of "bad apples"
            # NOTE: ALL active officers will return when looking for bad apples, however if the officer has no bad apple incidents will show them with a count of zero
            # Also NOTE: a copy of the object needs to be created, if not then if an officer is found within both dictionaries its count will be whatever amount is set lat
            bad_apples.append(copy.copy(active_officer_dict))

            # If the id of the officer is found with in good_egg_officer_count_by_id
            if(active_officer_dict['id'] in good_egg_officer_count_by_id):
                # Set the officers incident count to the calculated value
                active_officer_dict['count'] = good_egg_officer_count_by_id[active_officer_dict['id']]
            else:
                # Otherwise set the count to zero
                active_officer_dict['count'] = 0

            # Add officer to the list of "good eggs"
            # NOTE: ALL active officers will return when looking for good eggs, however if the officer has no good egg
            # incidents will show them with a count of zero
            # Also NOTE: a copy of the object needs to be created, if not then if an officer is found within both
            # dictionaries its count will be whatever amount is set lat
            good_eggs.append(copy.copy(active_officer_dict))

        # Get the JSON view context
        context = super(GoodEggsBadApples, self).get_context_data(**kwargs)

        # Sort the list of bad apples with the officers with the highest number of incidents displayed
        # first and add it to the responce
        context['bad_apples'] = sorted(
            bad_apples, key=lambda i: i['count'], reverse=True)

        # Sort the list of good eggs with the officers with the highest number of incidents displayed first
        # and add it to the responce
        context['good_eggs'] = sorted(
            good_eggs, key=lambda i: i['count'], reverse=True)

        # Return response
        return JsonResponse(context)


class RegistrationAPIView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = PersonSerializer

    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            person = serializer.save()
            # This method will return the serialized representations of new refresh
            #  and access tokens for the given person.
            refresh = RefreshToken.for_user(person)
            res = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
