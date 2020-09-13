from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Force, Officer, Incident
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model()

class ForceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Force
        fields = ('id', 'name', 'city', 'state',
                  'precinct_phone_number', 'precinct_address')


class OfficerSerializer(serializers.ModelSerializer):
    force_url = serializers.ModelSerializer.serializer_url_field(
        view_name='force_detail'
    )

    class Meta:
        model = Officer
        fields = ('id', 'first_name', 'last_name', 'dob', 'force',
                  'badge_number', 'nationality', 'race', 'gender', 'force_url')


class IncidentSerializer(serializers.ModelSerializer):
    user_url = serializers.ModelSerializer.serializer_url_field(
        view_name='user_detail'
    )

    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Incident
        fields = ('id', 'category', 'officers', 'date', 'time',
                  'location', 'description', 'formal_complaint', 'user_url', 'formal_complaint_number', 'user',  'witnesses_present', 'witnesses_information', 'private', 'bad_apple')
