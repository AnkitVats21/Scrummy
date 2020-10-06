import time
from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Cart, OrderItem, CheckoutAddress, Payment
from .serializers import CartSerializer, OrderItemSerializer, CheckoutAddressSerializer, PaymentSerializer
from accounts.serializers import FoodSerializer
from django.http import Http404
from accounts.models import Food, User

from cart import serializers

#Create your views here.

        

class OrderItemView(APIView):
    query_set           =   OrderItem.objects.all()
    serializer_class    = OrderItemSerializer, PaymentSerializer
    permission_classes   = (permissions.IsAuthenticated,)

    def get_food_data(self,data,request):
        food = FoodSerializer(data,context={'request': request})
        return food
    
    def verify_user(self,request):
        user = User.objects.filter(email__iexact=str(request.user))
        return int(user[0].id)

    def get(self, request, pk):
        id1=self.verify_user(request)
        if pk=='ordered':
            try:
                item=OrderItem.objects.filter(user__exact = id1).filter(ordered=True)
            except:
                raise Http404
            if item.exists():
                serializer = OrderItemSerializer(item, many=True,context={'request': request})
                for i in range(len(serializer.data)):
                    data        =item[i].item
                    food_item   = self.get_food_data(data,request)
                    serializer.data[i]['image']     =food_item.data['image']
                    serializer.data[i]['offer']     =food_item.data['offer']
                    serializer.data[i]['restaurent']=food_item.data['restname']
                # pay_data    = Payment.objects.filter(user=id1)
                # pay         = PaymentSerializer(pay_data, many=True)
                # serializer.data[0]['payment']=pay.data
                return Response(serializer.data)
            return Response(data={'details':'data not found'},status=status.HTTP_400_BAD_REQUEST)
        else:
            #item=OrderItem.objects.filter(user__exact = id1).filter(ordered=False)
            try:
                item=OrderItem.objects.filter(user__exact = id1).filter(ordered=False)
            except:
                raise Http404
            if item.exists():
                serializer = OrderItemSerializer(item, many=True,context={'request': request})
                for i in range(len(serializer.data)):
                    data=item[i].item
                    food_item = self.get_food_data(data,request)
                    serializer.data[i]['image']=food_item.data['image']
                    serializer.data[i]['offer']=food_item.data['offer']
                    serializer.data[i]['restaurent']=food_item.data['restname']
                return Response(serializer.data)
            return Response(data={'details':'data not found'},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        request_data=request.data
        user = request.user
        id1=self.verify_user(request)
        request_data['user']=id1
        item=OrderItem.objects.filter(user__exact = id1).filter(ordered=False)
        if pk=='checkout':
            for i in range(len(item)):
                food=item[i]
                food.ordered=True
                # food.ordered_date=date
                food.save()
            serializer = PaymentSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)       
            return Response(status=status.HTTP_400_BAD_REQUEST)         


class CheckoutAddressView(APIView):
    queryset            = CheckoutAddress.objects.all()
    serializer_class    = CheckoutAddressSerializer
    permission_classes  = (permissions.IsAuthenticated,)

    def verify_user(self,request):
        user = User.objects.filter(email__iexact=str(request.user))
        return int(user[0].id)

    def get(self,request):
        try:
            user = User.objects.filter(email=str(request.user))
            id = self.verify_user(request)
        except:
            raise Http404
        address = CheckoutAddress.objects.filter(user=id)
        serializer = CheckoutAddressSerializer(address,many=True)
        return Response(serializer.data)

    def post(self,request):
        address     = request.data
        serializer  = CheckoutAddressSerializer(data=address)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"detail":"invalid data"})

    def delete(self, request):
        add_id = request.data.get("id")
        try:
            add = CheckoutAddress.objects.filter(id=add_id)
        except:
            raise Http404
        add.delete()
        return Response(data={'details':'address deleted'})

class PaymentView(APIView):
    permission_classes=(permissions.IsAuthenticated)
    serializer_class = PaymentSerializer
    def verify_user(self,request):
        user = User.objects.filter(email__iexact=str(request.user))
        return int(user[0].id)
    def get(self, request):
        id1=self.verify_user(request)
        data = Payment.objects.filter(user=id1)
        serializer = PaymentSerializer(data, many=True)
        return Response(serializer.data)

# class OrderItemListView(APIView):
#     serializer_class = OrderItemSerializer

#     # def get_object(self, id):
#     #     try:
#     #         return OrderItem.objects.get(id = id)
#     #     except Cart.DoesNotExist:
#     #         raise Http404 

#     def get(self, request):
#         item = OrderItem.objects.all()
#         serializer = OrderItemSerializer(item, many=True,context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         data = request.data
#         serializer  = OrderItemSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class CheckoutView(APIView):
#     def get(self, request):
#         try:
#             address = CheckoutAddress.objects.filter(user=request.user)
#         except:
#             return Response(data={"details":"You don't have any saved address. Please add new one."},)
#         serializer = CheckoutAddressSerializer(address, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        

#     def post(self, request):
#         #print(request.data, request.user)
#         serializer = serializers.CheckoutAddressSerializer(request.data)
#         #print(serializer)
#         address = CheckoutAddress.objects.create(user=request.user, 
#         address=serializer.data.address, 
#         zip=serializer.data.zip)
#         return Response(serializer.data,status=status.HTTP_201_CREATED)

# class CartView(APIView):
#     serializer_class = CartSerializer
#     def get_object(self, pk):
#         try:
#             return Cart.objects.get(pk=pk)
#         except Cart.DoesNotExist:
#             raise Http404 

#     def get(self, request, pk):
#         cart = self.get_object(pk=pk)
#         serializer = CartSerializer(cart)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#         #return Response( serializers.errors, status = status.HTTP_400_BAD_REQUEST)