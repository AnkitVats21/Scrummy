from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    username    = models.CharField(blank=True, null=True, max_length = 30)
    email       = models.EmailField('email address', unique=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
        
  
class UserProfile(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name ='profile')
    name        = models.CharField(max_length = 30)
    address     = models.CharField(max_length = 200)
    picture     = models.ImageField(upload_to = 'pictures/', blank = True, null = True, max_length = 1000)
     
class OTP(models.Model):
    otp         = models.CharField(max_length = 6)
    otp_email   = models.EmailField(max_length= 255)