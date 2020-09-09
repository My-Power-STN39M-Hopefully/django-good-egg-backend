from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Force, Officer, Incident

class ForceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Force
        fields = ('id', 'name', 'city', 'state', 'precinct_phone_number', 'precinct_address')

class OfficerSerializer(serializers.ModelSerializer):
    force_url = serializers.ModelSerializer.serializer_url_field(
        view_name='force_detail'
    )
    class Meta:
        model = Officer
        fields = ('id', 'first_name', 'last_name', 'dob', 'force',
                  'badge_number', 'nationality', 'race', 'gender', 'force_url')


class UserSerializer(serializers.ModelSerializer):
    user_url = serializers.ModelSerializer.serializer_url_field(
        view_name='user_detail'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'user_url',
                  'last_name', 'email', 'is_staff', ]

class IncidentSerializer(serializers.ModelSerializer):
    officer_urls = serializers.ModelSerializer.serializer_url_field(
        view_name='officer_detail'
    )
    user_url = serializers.ModelSerializer.serializer_url_field(
        view_name='user_detail'
    )
    class Meta:
        model = Incident
        fields = ('id', 'category', 'officers', 'date', 'time', 'officer_urls',
                  'location', 'description', 'formal_complaint', 'user_url', 'formal_complaint_number', 'user',  'witnesses_present', 'witnesses_information', 'private', 'bad_apple')
