from django.shortcuts import render
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import permissions, viewsets, status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from cart.models import Cart, OrderItem, CheckoutAddress, Payment
from cart.serializers import CartSerializer, OrderItemSerializer, MyOrderSerializer, CheckoutAddressSerializer, PaymentSerializer
from accounts.serializers import FoodSerializer
from accounts.models import Food, User,Restaurent
from cart.models import OrderItem, MyOrder
from .serializers import EmployeeSerializer
from .models import Employee, Revenue
from .permissions import IsRestaurentOwner
from django.template.loader import render_to_string

class RestaurentOrderView(APIView):
    permission_classes = (permissions.IsAuthenticated,IsRestaurentOwner,)
    def get(self,request,pk):##pk==id showall/pk==id undelivered/pk==id delivered #id is rest_id action{showall,undelivered,delivered}
        rest_id,action      =   pk.split()
        if action=='showall':
            ordered_food    = MyOrder.objects.filter(ordered=True).filter(restaurant=rest_id)
            serializer      = MyOrderSerializer(ordered_food, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if action=='undelivered':
            ordered_food    = MyOrder.objects.filter(ordered=True,delivery_status=False).filter(restaurant=rest_id)
            serializer      = MyOrderSerializer(ordered_food, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if action=='delivered':
            ordered_food    = MyOrder.objects.filter(ordered=True,delivery_status=True).filter(restaurant=rest_id)
            serializer      = MyOrderSerializer(ordered_food, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self,request,pk):
        rest_id,order_id    = pk.split()
        ordered_food        = MyOrder.objects.filter(delivery_status=False).filter(restaurant=ffr.id)
        food=ordered_food.filter(id=pk)
        food.delivery_status==True
        food.save()
        #context      = {'':}
        # html_message = render_to_string('otp_template.html', context)
        # head         = ''
        # body         = ''
        # send_mail(head, str(body), 'in.scrummy@gmail.com', [user_email], html_message = html_message)
        return Response({"details":"Item delivered"})

class EmployeeRelatedView(viewsets.ModelViewSet):
    permission_classes  = (permissions.IsAuthenticated, IsRestaurentOwner,)
    serializer_class    = EmployeeSerializer
    queryset            = Employee.objects.all()

# class EmployeeTaskView(APIView):
#     permission_classes  = (permissions.IsAuthenticated, IsRestaurentOwner)

#     def get(self, request):

from cart.models import Payment
from cart.serializers import PaymentSerializer

class PaymentsView(APIView):
    permission_classes  = (permissions.IsAuthenticated, IsRestaurentOwner,)
    def get(self, request, pk):
        data        = Payment.objects.filter(id=pk)
        serializer  = PaymentSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

