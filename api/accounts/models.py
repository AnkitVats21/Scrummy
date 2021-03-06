from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.shortcuts import reverse


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have an email password')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    otp         = models.BooleanField(default=False)
    restaurent  = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):          
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    @property
    def otp_verified(self):
        return self.otp

    @property
    def is_restaurent(self):
        return self.restaurent
    
class UserProfile(models.Model):

    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name ='profile')
    name        = models.CharField(max_length = 30)
    address     = models.CharField(max_length = 200, blank=True, null=True)
    picture     = models.ImageField(upload_to = 'pictures/', blank = True, null = True, max_length = 1000)

    def __str__(self):
        return self.name
    
class OTP(models.Model):
    otp         = models.CharField(max_length = 6)
    otp_email   = models.EmailField(max_length= 255)
    time        = models.IntegerField()

    def __str__(self):
        return self.otp_email



class Restaurent(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE,related_name='owner', blank=True, null=True)
    restaurent_name     = models.CharField(unique=True, max_length=50, blank=False)
    restaurent_address  = models.CharField(max_length=200, blank=False)
    zip_code            = models.CharField(max_length=6, blank=False)
    description         = models.CharField(max_length=500, blank=False)
    wallpaper           = models.ImageField(max_length=2000, blank=True,null=True)
    rating              = models.CharField(default="5 1", max_length=30)
    def __str__(self):
        return self.restaurent_name
        
    def owner(self):
        return self.user.email
    def ratings(self):
        a=self.rating
        b=a.split()
        x=b[0]
        y=b[1]
        return str(int(x)/int(y))


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
        ('Sweets','Sweets'),
        ('Non-veg', 'Non-veg'),
    )

class Food(models.Model):
    rest_food       = models.ForeignKey(Restaurent, on_delete=models.CASCADE, related_name='restaurent_food', blank=True, null=True)
    name            = models.CharField(max_length=100, blank=False)
    price           = models.IntegerField(blank=False)
    rating          = models.CharField(max_length=20, default="5 1")
    image           = models.ImageField(max_length=2000,blank=True,null=True)
    delivery_time   = models.IntegerField(default=60,blank=False)
    cooking_time    = models.IntegerField(default=60,blank=True)
    offer           = models.PositiveIntegerField(default=0,blank=True, null=True)
    category        = models.CharField(choices= Category_choices, max_length=25)
    cuisine         = models.CharField(choices= Cuisine_choices, max_length=25)
    
    def __str__(self):
        return self.name

    def restname(self):
        # print(self.rest_food)
        return self.rest_food.restaurent_name
    def ratings(self):
        a=self.rating
        b=a.split()
        x=b[0]
        y=b[1]
        return str(int(x)/int(y))

class FoodSearch(models.Model):
    word        = models.CharField(max_length=30)
    frequency   = models.IntegerField(default=0)

    def __str__(self):
        return self.word
