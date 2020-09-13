from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from users.models import CustomUser
from .managers import CustomUserManager
from django.contrib.auth.base_user import BaseUserManager

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name',
                  'last_name', 'nationality', 'gender', 'race', 'city', 'state', 'phone_number', 'password']
        #extra_kwargs = {'password': {'write_only': True}}