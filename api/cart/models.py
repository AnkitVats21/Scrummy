from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from accounts.models import User, Food


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
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
    

class Cart(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    items       = models.ManyToManyField(OrderItem)
    start_date  = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    ordered_date= models.DateTimeField(blank=True,null=True)
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
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    # def __str__(self):
    #     return self.user.get_email_field_name


#     foods     = models.ManyToManyField(Food)
#     quantity = models.IntegerField(default=1)
#     order_time  = models.DateTimeField(auto_now_add=True, null=True)
#     ordered     = models.BooleanField(default=False)
#     def __str__(self):
#         return str(self.foods.name)


# class Order(models.Model):
#     user        = models.OneToOneField(User, on_delete=models.CASCADE)
#     items       = models.ForeignKey(OrderItem, on_delete=models.CASCADE, blank=True, null=True)

#     def __str__(self):
#         return str(self.user)


# class MyOrders(models.Model)
    