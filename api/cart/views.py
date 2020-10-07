import time
from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import Cart, OrderItem, CheckoutAddress, Payment, MyOrder
from .serializers import CartSerializer, OrderItemSerializer, CheckoutAddressSerializer, PaymentSerializer, MyOrderSerializer
from accounts.serializers import FoodSerializer
from django.http import Http404, HttpResponse
from accounts.models import Food, User, Restaurent
from django.core.mail import send_mail
from cart import serializers
from django.shortcuts import render
from django.template import Context, loader
from django.template.loader import render_to_string
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
        if pk=='wishlist':
            try:
                item=OrderItem.objects.filter(user__exact = id1).filter(ordered=False)
            except:
                raise Http404
            if item.exists():
                serializer = MyOrderSerializer(item, many=True,context={'request': request})
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
        if pk=='show':
    
            try:
                item=OrderItem.objects.filter(user__exact = id1).filter(ordered=True)
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
        return Response(data={"error":"bad request"}, status=status.HTTP_400_BAD_REQUEST)

##############################################################
#                      for checkout                          #
##############################################################
    def post(self, request, pk):
        request_data=request.data
        try:
            user_email=str(request.user)
        except:
            pass
        user = request.user #not needed yet
        id1=self.verify_user(request)
        request_data = request_data.copy()
        request_data['user'] = id1
        try:
            item=OrderItem.objects.filter(user__exact = id1).filter(ordered=True)
        except:
            raise Http404
        if pk=='checkout' and len(item):
            amount=0
            discounted_price=0
            order_summary="S. No.\tItem Name\t\tPrice\t\tDiscounted Price\n"
            summary=[]
            
            for i in range(len(item)):
                food=item[i]
                a=int(food.quantity)*int(food.item.price)
                amount += a
                b=int(food.quantity)*int(food.item.price)*((100-int(food.item.offer))/100)
                discounted_price += b
                obj = MyOrder.objects.create(user=food.user, ordered=True, item = food.item, quantity = food.quantity)
                obj.save()
                o_d={}
                o_d["sno"]=i+1
                o_d["item_name"]=food.item_name()
                o_d["quantity"]=food.quantity
                o_d["price"]=food.item.price
                o_d["offer"]=food.item.offer
                o_d["discount_price"]=b
                summary.append(o_d)
                order_summary += ("{}.\t{}\t\t{}x{}={}\t{}\n").format(i+1,str(food.item_name()), str(food.quantity),str(food.item.price),a,b )
            r=item[0].restaurant
            print(r)
            context= {
            'summary': summary,
            'total': discounted_price,
            'restaurant': r,
            'name': request.user.profile.name
            }
            template = loader.get_template('email_template.html') # getting our template  
            html_message = render_to_string('email_template.html', context)
            order_summary += ("\t\t\t\tTotal\t\t{}\n").format(discounted_price)
            #print(amount," ",discounted_price)
            restname=item[0].restaurant
            id2 = Restaurent.objects.filter(restaurent_name=restname)[0].id
            request_data['restaurant']=id2
            request_data['amount']=amount
            request_data['discounted_price']=discounted_price
            serializer = PaymentSerializer(data=request_data)
            #item.delete()
            if serializer.is_valid():
                serializer.save()
                print(user_email)
                if user_email:
                    head = ("Your Scrummy order from {}").format(restname)
                    body = ("Hello {}!\nYour order summary\nOrder ID: SCN00{} \nWe hope you have enjoyed your meal from {}.").format(request.user.profile.name,serializer.data.get('id'),restname)
                    send_mail(head, str(body), 'in.scrummy@gmail.com', [user_email], html_message = html_message)
                return Response(serializer.data, status=status.HTTP_201_CREATED)       
            return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)    
        return Response(data={"details":"please add some food item in your cart before you checkout"} ,status=status.HTTP_400_BAD_REQUEST)    



class CheckOrderStatus(APIView):
    def verify_user(self,request):
        user = User.objects.filter(email__iexact=str(request.user))
        return int(user[0].id)
    #pk is the id of the food
    def get(self, request, pk):
        id1     =self.verify_user(request)
        try:
            orders  = OrderItem.objects.filter(user=id1).filter(item=pk).filter(ordered=False)
            if orders.exists():
                return Response(data={"details":"item in your cart"}, status=status.HTTP_302_FOUND)
            return Response(data={"details":"item not in your cart"}, status=status.HTTP_404_NOT_FOUND)
        except:
            raise Http404

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
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class = PaymentSerializer
    def verify_user(self,request):
        user = User.objects.filter(email__iexact=str(request.user))
        return int(user[0].id)
    def get(self, request):
        id1=self.verify_user(request)
        data = Payment.objects.filter(user=id1)
        serializer = PaymentSerializer(data, many=True)
        return Response(serializer.data)

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

class MyOrderView(APIView):
    serializer_class = MyOrderSerializer

    def verify_user(self,request):
        user = User.objects.filter(email__iexact=str(request.user))
        return int(user[0].id)

    def get_food_data(self,data,request):
        food = FoodSerializer(data,context={'request': request})
        return food

    def get(self, request):
        id1     =self.verify_user(request)
        # item = OrderItem.objects.filter(id=id1)
        try:
            item=MyOrder.objects.filter(user__exact = id1).filter(ordered=True)
        except:
            raise Http404
        if item.exists():
            serializer = MyOrderSerializer(item, many=True,context={'request': request})
            for i in range(len(item)):
                data=item[i].item
                food_item = self.get_food_data(data,request)
                serializer.data[i]['image']=food_item.data['image']
                serializer.data[i]['offer']=food_item.data['offer']
                serializer.data[i]['restaurent']=food_item.data['restname']
            return Response(serializer.data, status=status.HTTP_302_FOUND)
        return Response(data={'details':'data not found'},status=status.HTTP_404_NOT_FOUND)
        # serializer = MyOrderSerializer(item, many=True,context={'request': request})
        # return Response(serializer.data)

    # post request for developers use only
    def post(self, request):
        data = request.data
        serializer  = OrderItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
