from django.shortcuts import render
import time
from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

# Create your views here.

class OrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'details':'error'}, status=status.HTTP_400_BAD_REQUEST)



class OrderItemView(APIView):

    # def get(self,request,id)
    def post(self, request):
        serializer = OrderItemSerializer(request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'details':'error'}, status=status.HTTP_400_BAD_REQUEST)
    