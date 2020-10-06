from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from accounts.models import User, Food
from django.core.validators import RegexValidator


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    ordered_date= models.DateTimeField(blank=True,null=True)
    item = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"
    def username(self):
        return self.user.email

    def get_total_item_price(self):
        return self.quantity * self.item.price
    def item_name(self):
        return self.item.name
   
    def delivery_time(self):
        return self.item.delivery_time
    

class Cart(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    items       = models.ManyToManyField(OrderItem)
    ordered_date= models.DateTimeField(blank=True,null=True)
    start_date  = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    ordered     = models.BooleanField(default=False)
    def __str__(self):
        return self.user.email
    
    def username(self):
        return self.user.email

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total
    def items_name(self):
        return self.items.name
    


class MyOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    ordered_date= models.DateTimeField(auto_now=True, blank=True,null=True)
    item = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"
    
class CheckoutAddress(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_regex     = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone           = models.CharField(validators=[phone_regex], max_length=17, blank=True)  
    address         = models.CharField(max_length=100)
    zip             = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email


class Payment(models.Model):
    user        = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount      = models.FloatField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email