from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import ugettext_lazy  as _


#user and authentication related model
class User(AbstractUser):
    class UserType(models.IntegerChoices):
        CUSTOMER   = 1
        RESTAURENT = 2
    first_name  = models.CharField(blank=True, null=True, max_length = 30)
    last_name   = models.CharField(blank=True, null=True, max_length = 30)
    email       = models.EmailField('email address', unique=True)
    username    = models.CharField(blank=True, null=True, max_length=10)
    is_active   = models.BooleanField(_('active'), default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    Role        = models.IntegerField(choices=UserType.choices, default=1)
    is_restaurent   = models.BooleanField(default=False)
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email
        
# class Customer(models.Model):
#     user        = models.OneToOneField(User, on_delete=models.CASCADE)
#     address     = models.OneToOneField(Address)
#     orders      = models.OneToOneField(Order )


class UserProfile(models.Model):

    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name ='profile')
    name        = models.CharField(max_length = 30)
    address     = models.CharField(max_length = 200)
    #picture     = models.ImageField(upload_to = 'pictures/', blank = True, null = True, max_length = 1000)



class OTP(models.Model):
    otp         = models.CharField(max_length = 6)
    otp_email   = models.EmailField(max_length= 255)
    time        = models.IntegerField()
    
    def __str__(self):
        return self.otp_email
    


#restaurent related models

class Restaurent(models.Model):
   
    restaurent_name      = models.CharField(unique=True, max_length=50, blank=False)
    restaurent_address   = models.CharField(max_length=200, blank=False)
    zip_code     = models.CharField(max_length=6, blank=False)
    description = models.CharField(max_length=500, blank=False)

    def __str__(self):
        return self.restaurent_name

class Food(models.Model):
    Rating_choices = (
    (1, 'Poor'),
    (2, 'Average'),
    (3, 'Good'),
    (4, 'Very Good'),
    (5, 'Excellent'),
    )

    Category_choices =( 
        ( 1, 'Bakery'),
        (2, 'Bengali'), (3, 'Biryani'), (4, 'Cafe'),
        (5, 'Chaat'), (6, 'Chinese'),  (7, 'Desserts'),
        (8, 'Fast Food'), (9, 'French'), (10, 'Ice Cream'),
        (11, 'Indian'), (12, 'Italian'),(13, 'Kebabs'),
        (14, 'Lucknowi'), (15, 'Maharashtrian'),
        (16, 'Mexican'), (17, 'Mughlai'), (18, 'North Indian'),
        (19, 'Pastas'), (20, 'Pizzas'), (21, 'Punjabi'),
        (22, 'Rajasthani'), (23, 'Snacks'), (24,'South Indian'), 
        (25, 'Street Food'), (26, 'Sweets'), (27, 'Tandoor'),
        (28, 'Thalis'),
    )

    Cuisine_choices =(
        (1, "North Indian"),
        (2, "South Indian"),
        (3, "Chinese"),
        (4, "Italian"),
        (5, "French"),
        (6, "Punjabi"),
    )

    restaurent  = models.ForeignKey(Restaurent, on_delete=models.CASCADE)
    name        = models.CharField(max_length=100, blank=False)
    price       = models.IntegerField(blank=False)
    rating      = models.IntegerField(choices=Rating_choices, default=5)
    #cuisine     = models.ForeignKey(Cuisine, on_delete=models.SET_NULL)
    image       = models.ImageField(max_length=2000)
    #prep_time   = models.TimeField()
    offer       = models.PositiveIntegerField(default=0)
    category    = models.IntegerField(choices= Category_choices)
    
    cuisine     = models.IntegerField(choices= Cuisine_choices)

    def __str__(self):
        return self.name
    


# class Cuisine(models.Model):
#     # food            = models.
#     cuisine_name    = models.CharField(max_length=20)


# #user related models

# class Cart(models.Model):
#     user            =models
#     food            =


# class MyOrders(models.Model):
#     user            =
#     food            =


