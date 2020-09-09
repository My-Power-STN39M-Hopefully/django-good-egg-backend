from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Force


class ForceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Force
        fields = ('id', 'name', 'city', 'state', 'precinct_phone_number', 'precinct_address')
