from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Force, Officer

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
