from rest_framework import serializers
from .models import Force, Officer, Incident
from django.contrib.auth import authenticate
from users.models import CustomUser
from django.contrib.auth import get_user_model

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

    def create(self, validated_data):
        user = CustomUser.objects.get(id=self.context['request'].user.id)
        validated_data['user'] = user
        return super(IncidentSerializer, self).create(validated_data)
    

    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Incident
        fields = ('id', 'category', 'officers', 'date', 'time', 'officer_urls',
                  'location', 'description', 'formal_complaint', 'user_url', 'formal_complaint_number',  'witnesses_present', 'witnesses_information', 'private', 'bad_apple', 'user')
        write_only_fields = ('user',)
