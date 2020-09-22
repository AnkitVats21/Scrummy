from rest_framework import serializers
from .models import User, UserProfile
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
class UserProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserProfile
        fields = ('name','address', 'picture')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'profile',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.name = profile_data.get('name', profile.name)
        profile.address = profile_data.get('address', profile.address)
        profile.picture = profile_data.get('picture', profile.picture)
        profile.save()

        return instance

