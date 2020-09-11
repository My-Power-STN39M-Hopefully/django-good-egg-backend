from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Force, Officer, Incident, Person
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
User = get_user_model()


class PersonSerializer(serializers.ModelSerializer):

    person_url = serializers.ModelSerializer.serializer_url_field(
        view_name='person_detail')

    def get(self, validated_data):
        self.first_name = self.user.first_name
        return self

    class Meta:
        model = Person
        fields = ['person_url',
                  'phone_number', 'race', 'nationality', 'gender', 'city', 'state', 'user', ]


def create(self, validated_data):

    username = validated_data['user.username']
    first_name = validated_data['user.first_name']
    last_name = validated_data['user.last_name']
    email = validated_data['user.email']
    password = validated_data['user.password']
    user = User(email=email, first_name=first_name,
                last_name=last_name, password=password, username=username)
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
