from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from accounts.models import User, Food


class OrderItem(models.Model):
    item     = models.ForeignKey(Food, on_delete=models.CASCADE)
    # quantity = models.IntegerField(default=1)
    def __str__(self):
        return str(self.item)


class Order(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    items       = models.ManyToManyField(OrderItem)
    order_time  = models.DateTimeField(auto_now_add=True)
    ordered     = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

# class MyOrders(models.Model)
    