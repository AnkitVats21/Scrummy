from rest_framework import serializers
from .models import User, UserProfile, OTP, Restaurent, Food
from django.contrib.auth import authenticate
#from rest_framework_jwt.settings import api_settings
class OTPSerializer(serializers.ModelSerializer):

    class Meta:
        model = OTP
        fields = ('otp_email','otp')

class UserProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserProfile
        fields = ('name','address','picture')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'profile','restaurent')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     profile = instance.profile

    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()

    #     profile.name = profile_data.get('name', profile.name)
    #     profile.address = profile_data.get('address', profile.address)
    #     # profile.picture = profile_data.get('picture', profile.picture)
    #     profile.save()

    #     return instance

class RestaurentSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Restaurent
        fields = ('id','user','restaurent_name','zip_code','restaurent_address','description',)

    def create(self, validated_data):
        # restaurent_owner = validated_data.pop('user')
        # print(restaurent_owner)
        # try:
        #     user = User.objects.filer(email=restaurent_owner)
        # except:
        #     return 'user not found'
        # print('user found')
        # restaurent.user=resturent_owner
        restaurent = Restaurent(**validated_data)
        restaurent.save()
        return restaurent

class FoodSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:food-detail")
    class Meta:
        model   = Food
        fields = ('id','url','name',
        'image','price',
        'rating','offer','category',
        'cuisine','delivery_time','rest_food_id','restname',)
    # def create(self, validated_data):
# 'rest_food',