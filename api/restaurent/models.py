from django.db import models
from accounts.models import Food

class Employee(models.Model):
    name           = models.CharField(max_length=30)
    service_status = models.BooleanField(default=False)
    