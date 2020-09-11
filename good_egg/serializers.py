from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Force, Officer, Incident
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'phone_number', 'race',
                  'nationality', 'gender', 'gender', 'city', 'state')

    def create(self, validated_data):

        name = validated_data['name']
        email = validated_data['email']
        password = validated_data['password']
        user = User(email=email, name=name)
        # Sets the user’s password to the given raw string,
        # taking care of the password hashing. Doesn’t save the User object.

        user.set_password(password)

        # save() method to save the user object
        user.save()

        return user


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
