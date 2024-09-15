from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, UserPreferences

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    pin = serializers.CharField(write_only=True, max_length=6)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'pin']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            pin=validated_data['pin'],
            password=validated_data['password']
        )
        return user

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = '__all__'