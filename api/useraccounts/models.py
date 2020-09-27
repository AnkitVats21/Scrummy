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
        return self.otp_email + " OTP"
    



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
        ( 'Bakery', 'Bakery'),
        ('Bengali', 'Bengali'), ('Biryani', 'Biryani'), ('Cafe', 'Cafe'),
        ('Chaat', 'Chaat'), ('Chinese', 'Chinese'),  ('Desserts', 'Desserts'),
        ('Fast Food', 'Fast Food'), ('French', 'French'), ('Ice Cream', 'Ice Cream'),
        ('Indian', 'Indian'), ('Italian', 'Italian'),('Kebabs', 'Kebabs'),
        ('Lucknowi', 'Lucknowi'), ('Maharashtrian', 'Maharashtrian'),
        ('Mexican', 'Mexican'), ('Mughlai', 'Mughlai'), ('North Indian', 'North Indian'),
        ('Pastas', 'Pastas'), ('Pizzas', 'Pizzas'), ('Punjabi', 'Punjabi'),
        ('Rajasthani', 'Rajasthani'), ('Snacks', 'Snacks'), ('South Indian','South Indian'), 
        ('Street Food', 'Street Food'), ('Sweets', 'Sweets'), ('Tandoor', 'Tandoor'),
        ('Thalis', 'Thalis'),
    )

    Cuisine_choices =(
        ('North Indian', "North Indian"),
        ('South Indian', "South Indian"),
        ('Chinese', "Chinese"),
        ('Italian', "Italian"),
        ('French', "French"),
        ('Punjabi', "Punjabi"),
    )

    restaurent  = models.ForeignKey(Restaurent, on_delete=models.CASCADE, default=1)
    name        = models.CharField(max_length=100, blank=False)
    price       = models.IntegerField(blank=False)
    rating      = models.IntegerField(choices=Rating_choices, default=5)
    image       = models.ImageField(max_length=2000)
    delivery_time   = models.IntegerField(default=60,blank=False)
    offer       = models.PositiveIntegerField(default=0)
    category    = models.CharField(choices= Category_choices, max_length=25)
    cuisine     = models.CharField(choices= Cuisine_choices, max_length=25)

    def __str__(self):
        return self.name