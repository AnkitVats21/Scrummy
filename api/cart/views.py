import time
from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Cart,MyOrder,OrderItem,CheckoutAddress,Payment
from .serializers import CartSerializer, OrderItemSerializer, MyOrderSerializer

#Create your views here.

class CartView(APIView):
    serializer_class = CartSerializer

    def get(self, request):
        cart = Cart.objects.all()
        serializer = CartSerializer(cart)
        return Response(serializer.data,status=status.HTTP_200_OK)
        #return Response( serializers.errors, status = status.HTTP_400_BAD_REQUEST)
        

class OrderItemView(APIView):
    query_set   =   OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_object(self, id):
        try:
            #print(OrderItem.objects.filter(user = id))
            return OrderItem.objects.filter(user__exact = id)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        item = self.get_object(id=id)
        serializer = OrderItemSerializer(item, many=True)
        return Response(serializer.data)

from cart import serializers
class CheckoutView(APIView):
    def get(self, request):
        try:
            address = CheckoutAddress.objects.filter(user=request.user)
        except:
            return Response(data={"details":"You don't have any saved address. Please add new one."},)
        serializer = serializers.CheckoutAddressSerializer(address, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self, request):
        print(request.data, request.user)
        serializer = serializers.CheckoutAddressSerializer(request.data)
        print(serializer)
        address = CheckoutAddress.objects.create(user=request.user, 
        address=serializer.data.address, 
        zip=serializer.data.zip)
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class MyOrderListView(APIView):
    def get(self, request):
        orders = MyOrder.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        # if orders.exists():

        

    # def post(self, request, pk):
    #     item = get_object_or_404(Food, id=pk)
    #     #print(item,request.user)
    #     order_item, created = OrderItem.objects.get_or_create(item = item, user = request.user, ordered = False)
    #     cart_qs = Cart.objects.filter(user=request.user, ordered=False)
    #     #print(cart_qs)
    #     if cart_qs.exists():
    #         order = cart_qs[0]
    #         if order.items.filter(item__pk=item.pk).exists():
    #             order_item.quantity += 1
    #             order_item.save()
    #             return Response(data={'details':"item added to cart"},status=status.HTTP_201_CREATED)
    #         else:
    #             order.items.add(order_item)
    #             return Response(data={'details':"item added to cart"},status=status.HTTP_201_CREATED)
    #     else:
    #         ordered_date = timezone.now()
    #         order       = Cart.objects.create(user=request.user, ordered_date=ordered_date)
    #         order.items.add(order_item)
    #         return Response(data={"details":"item added to your cart"})


        

# class MyOrderView(APIView):
#     serializer_class = MyOrdersSerializer

#     def get(self, request):
#         serializer  =   MyOrdersSerializer()

#     def post(self, request):
#         serializer = OrderSerializer(request.data)
#         if serializer.is_valid():
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({'details':'error'}, status=status.HTTP_400_BAD_REQUEST)
    

#     def post(self, request):
#         serializer = CartSerializer(request.data, many=True)
#         if serializer.is_valid():
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({'details':'error'}, status=status.HTTP_400_BAD_REQUEST)
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