from .models import Employee, Revenue
from rest_framework import serializers

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Employee
        fields  = '__all__'

class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Revenue
        fields  = '__all__'