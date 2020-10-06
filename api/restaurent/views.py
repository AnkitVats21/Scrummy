from django.shortcuts import render
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from cart.models import Cart, OrderItem, CheckoutAddress, Payment
from cart.serializers import CartSerializer, OrderItemSerializer, CheckoutAddressSerializer, PaymentSerializer
from accounts.serializers import FoodSerializer
from django.http import Http404
from accounts.models import Food, User
from cart.models import OrderItem

class RestaurentOrderView(APIView):
    def get(self,request,pk):
        ordered_food    = OrderItem.objects.filter(ordered=True)
        serializer      = OrderItemSerializer(ordered_food, many=True)
        print(ordered_food)
        return Response(serializer.data)
        try:
            food_from_restaurent = Restaurent.objects.filter(restaurent_name__iexact=pk)
            rest_id         = food_from_restaurent[0].id
            # food            = Food.objects.filter(rest_food=int(rest_id))
            ordered_food    = OrderItem.objects.filter(ordered=True)
            # ordered_food    = ordered_food.intersection(food)
        except:
            raise Http404
