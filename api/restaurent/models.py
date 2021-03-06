from django.db import models
from accounts.models import Food, User,Restaurent

class Employee(models.Model):
    name           = models.CharField(max_length=30)
    restaurant     = models.OneToOneField(Restaurent,on_delete=models.CASCADE)
    details        = models.CharField(max_length=500)
    service_status = models.BooleanField(default=False)

    def __str__(self):
        return self.restaurant.restaurent_name+":employee name-->"+self.name
    
    
class Revenue(models.Model):
    amount          = models.FloatField()
    owner           = models.OneToOneField(User,on_delete=models.CASCADE)
    user            = models.ForeignKey(User,on_delete=models.CASCADE, related_name="customer")
    restaurant      = models.ForeignKey(Restaurent,on_delete=models.CASCADE)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "paid by --> "+str(self.user.email)+" to -->"+self.restaurant.restaurent_name     

class Feedback(models.Model):
    rate_choices=(
        (1,"VERY BAD"),
        (2,"BAD"),
        (3,"GOOD"),
        (4,"VERY GOOD"),
        (5,"EXCELLENT"),
    )
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    rate_count  = models.IntegerField(choices=rate_choices)
    review      = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.user) + " --> "+ str(self.rate_count)
    