from django.shortcuts import render
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from cart.models import Cart, OrderItem, CheckoutAddress, Payment
from cart.serializers import CartSerializer, OrderItemSerializer, MyOrderSerializer, CheckoutAddressSerializer, PaymentSerializer
from accounts.serializers import FoodSerializer
from rest_framework import status
from django.http import Http404
from accounts.models import Food, User,Restaurent
from cart.models import OrderItem, MyOrder

class RestaurentOrderView(APIView):
    def get(self,request,pk):
        user        = request.user
        restaurant  =   Restaurent.objects.filter(user=request.user)
        if user.restaurent:
            ffr             = Restaurent.objects.filter(restaurent_name__iexact=pk)
            ordered_food    = MyOrder.objects.filter(ordered=True).filter(restaurant=ffr.id)
            serializer      = MyOrderSerializer(ordered_food, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data={"details":"not a restaurent owner"})
        

    def post(self,request,pk):
        user        = request.user
        restaurant  =   Restaurent.objects.filter(user=request.user)
        if user.restaurent:
            ffr             = Restaurent.objects.filter(restaurent_name__iexact=pk)
            ordered_food    = MyOrder.objects.filter(delivery_status=False).filter(restaurant=ffr.id)
            idf=request.data.get('ids')
            for i in idf:
                food=ordered_food.filter(id=i)
                food.delivery_status==True
                food.save()
            return Response({"details":"Item delivered"})

clas