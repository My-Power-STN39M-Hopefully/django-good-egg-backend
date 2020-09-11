from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name',
                  'last_name', 'nationality', 'gender', 'race', 'city', 'state', 'phone_number']
