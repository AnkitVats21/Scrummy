import time
from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Cart,MyOrder,OrderItem
from .serializers import CartSerializer, MyOrderSerializer, OrderItemSerializer

#Create your views here.


class CartView(APIView):
    serializer_class = CartSerializer
    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404 

    def get(self, request, pk):
        cart = self.get_object(pk=pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data,status=status.HTTP_200_OK)
        #return Response( serializers.errors, status = status.HTTP_400_BAD_REQUEST)
        

class OrderItemView(APIView):
    serializer_class = OrderItemSerializer

    def get_object(self, id):
        try:
            return OrderItem.objects.get(id = id)
        except Cart.DoesNotExist:
            raise Http404 

    def get(self, request, id):
        item = self.get_object(id=id)
        serializer = OrderItemSerializer(item)
        return Response(serializer.data)

    # def post(self, request, id):


class OrderItemListView(APIView):
    serializer_class = OrderItemSerializer

    # def get_object(self, id):
    #     try:
    #         return OrderItem.objects.get(id = id)
    #     except Cart.DoesNotExist:
    #         raise Http404 

    def get(self, request):
        item = OrderItem.objects.all()
        serializer = OrderItemSerializer(item, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer  = OrderItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# class MyOrderView(APIView):
#     serializer_class = MyOrdersSerializer

#     def get(self, request):
#         serializer  =   MyOrdersSerializer()

#     def post(self, request):
#         serializer = OrderSerializer(request.data)
#         if serializer.is_valid():
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({'details':'error'}, status=status.HTTP_400_BAD_REQUEST)
    


    # def post(self, request):
    #     serializer = CartSerializer(request.data, many=True)
    #     if serializer.is_valid():
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response({'details':'error'}, status=status.HTTP_400_BAD_REQUEST)