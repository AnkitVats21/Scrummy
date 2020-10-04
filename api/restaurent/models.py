from django.db import models
from accounts.models import food

class Sale(models.Model):
    prodect     = models.ManyToManyField(Food)
    quantity    = models.CharField(default=1)
    
