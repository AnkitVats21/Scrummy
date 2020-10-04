import time
from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import User, OTP, Food, Restaurent
from .serializers import UserSerializer, OTPSerializer, FoodSerializer, RestaurentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import check_password
#from .permissions import UserPermission, UserDetailPermissions
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from random import randint
from django.core.mail import send_mail


class VerifyOTP(APIView):
    queryset = OTP.objects.all()
    serializer_class = OTPSerializer

    def post(self, request):
        request_data = request.data
        request_otp  = request_data.get("otp", "")
        request_email= request_data.get("otp_email", "")
        t1           = int(time.time())

        try:
            obj = OTP.objects.filter(otp_email__iexact = request_email)[0]
        except:
            data = {"error":"OTP object not found"}
            return Response(data,status=status.HTTP_404_NOT_FOUND)

        stored_db_email  = obj.otp_email 
        stored_db_otp    = obj.otp
        t2               = obj.time

        if (t1-t2)>300:
            obj.delete()
            data = {"error":"otp expired"}
            return Response(data,status = status.HTTP_404_NOT_FOUND)
        elif stored_db_email == request_email and stored_db_otp == request_otp:
            data = {"details":"otp verified"}
            try:
                user = User.objects.filter(email__iexact = request_email)[0]
            except:
                data = {"details":"email not found in users"}
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            user = User.objects.filter(email__iexact = request_email)[0]
            user.active=True
            user.otp=True
            user.save()
            obj.delete()
            return Response(data , status = status.HTTP_200_OK)
        return Response(data={"error":"wrong otp"},status = status.HTTP_404_NOT_FOUND)

# class LoginView(APIView):

        


class UserAccountsList(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        users       = User.objects.all()
        serializer  = UserSerializer(users, many = True)
        return Response(serializer.data)

class CreateUserAccount(APIView):
    #queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request):
        user_email  = request.data.get("email")
        req_data    =request.data
        if check(user_email):
            user = User.objects.filter(email__iexact = user_email)
            
            if user.exists():
                data = {"error":"User with the given email address already exists"}
                return Response(data, status = status.HTTP_226_IM_USED)
            else:
                    otp = randint(1000, 9999) 
                    t = int(time.time())
                    OTP.objects.create(otp = otp, otp_email = user_email, time= t)
                    body = ("Hello! Your one time password verification for registering in Scrummy is {}").format(otp)

                    send_mail('OTP Verification', body, 'in.scrummy@gmail.com', [user_email], fail_silently = False)
                    serializer = UserSerializer(data = req_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status = status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                    data = {"details":"OTP sent successfully"}
                    return Response(data, status = status.HTTP_200_OK)
        else:
            data = {"error":"Please enter valid email"}
            return Response(data, status = status.HTTP_400_BAD_REQUEST)

class ResetPasswordOTP(APIView):
    def post(self, request):
        user_email = request.data.get("email")
        request_otp = request.data.get("otp")
        print(user_email,request_otp)
        #user = User.objects.filter(email__iexact = user_email)[0]
        try:
            obj = OTP.objects.filter(otp_email__iexact = user_email)[0]
        except:
            data = {"error":"wrong email"}
            return Response(data,status=status.HTTP_404_NOT_FOUND)
        t1 = time.time()
        stored_db_email  = obj.otp_email 
        stored_db_otp    = obj.otp
        t2               = obj.time

        if (t1-t2)>3000:
            obj.delete()
            data = {"error":"otp expired"}
            return Response(data,status = status.HTTP_404_NOT_FOUND)
        if stored_db_otp == request_otp:
            obj.delete()
            return Response(data={'details':'OTP Verified'})
        return Response(data={"error":"wrong OTP"}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPassword(APIView):
    def post(self, request):
        request_email       = request.data.get('email')
        request_password    = request.data.get('password')
        print(request_email, "pass:", request_password)
        try:
            user = User.objects.filter(email__iexact = request_email)[0]
        except:
            data = {"error":"wrong email"}
            return Response(data,status=status.HTTP_404_NOT_FOUND)
        user = User.objects.filter(email__iexact = request_email)[0]
        user.set_password(request_password)
        user.save()
        return Response(data={"details":"password reset"}, status = status.HTTP_200_OK)


class UserAccountsDetails(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, id):
        
        try:
            return User.objects.get(id = id)
        except User.DoesNotExist:
            return Response({'details':'user not found'})
    def get(self, request, id):

        user_id=request.user.id
        data = {"error":"Access Denied"},
        if user_id==id:
            user = self.get_object(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response( data, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        user_id=request.user.id
        data = {"error":"Access Denied"},
        if user_id==id:
            user = self.get_object(id=id)
            serializer = UserSerializer(user, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_200_OK)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response(data, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        data = {"error":"Access Denied"},
        user_id=request.user.id
        if user_id==id:
            user = self.get_object(id)
            user.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        return Response(data , status = status.HTTP_400_BAD_REQUEST)

    
class GenerateOTP(APIView):
    def post(self, request):
        user_email = request.data.get("email")
        print(user_email)
        try:
            user= User.objects.filter(email__iexact = user_email)[0]
        except:
            return Response(data={"error":"User not found with given email"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            obj = OTP.objects.filter(otp_email__iexact = user_email)[0]
            obj.delete()
        except:
            if check(user_email):
                t=int(time.time())
                otp = randint(1000, 9999) 
                body = ("Hello! Your OTP is {}. Do not share it with anyone.").format(otp)
                OTP.objects.create(otp = otp, otp_email = user_email, time =t)
                send_mail('OTP Verification', body, 'in.scrummy@gmail.com', [user_email], fail_silently = False)
                data = {"details":"OTP sent succesfully"}
                return Response(data, status = status.HTTP_200_OK)
            else:
                data = { "error":"invalid email"}
                return Response( data, status = status.HTTP_406_NOT_ACCEPTABLE)

        if check(user_email):
            t=int(time.time())
            otp = randint(1000, 9999) 
            body = ("Hello! Your OTP is {}. Do not share it with anyone.").format(otp)
            OTP.objects.create(otp = otp, otp_email = user_email, time =t)
            send_mail('OTP Verification', body, 'in.scrummy@gmail.com', [user_email], fail_silently = False)
            data = {"details":"OTP sent succesfully"}
            return Response(data, status = status.HTTP_200_OK)
        else:
            data = { "error":"invalid email"}
            return Response( data, status = status.HTTP_406_NOT_ACCEPTABLE)
        
class CheckOTPVerifiedStatus(APIView):
    def post(self , request, **args):
        request_email = request.data.get('email')
        request_password = request.data.get('password')
        try:
            user = User.objects.filter(email__iexact = request_email)[0]
            
        except:
            data = {"error":"email not found in users"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.filter(email__iexact = request_email)[0]

        if user.check_password(request_password):
            if user.otp:
                return Response(data={"details":"user otp verified"}, status=status.HTTP_200_OK)
            return Response(data={"error":"user is not otp verified"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(data={'detail':'wrong password'},status=status.HTTP_400_BAD_REQUEST)

#validating email

import re 
  
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def check(email):  
    if(re.search(regex,email)):  
        return True   
    else:  
        return False


###########################################################################

            #FOOD RELATED VIEWS 

###########################################################################

class FoodList(APIView):
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)
    queryset = Food.objects.all()
    serializer_class  = FoodSerializer
    def get(self, request):
        try:
            food = Food.objects.all()
        except:
            return Response(data={"detais":"object not found"}, status=status.HTTP_204_NO_CONTENT)
        serializer = FoodSerializer(food, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        food_data   = request.data
        serializer = FoodSerializer(data=food_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(data={"details":"please enter valid data"})

        

class FoodView(APIView):
    # permission_classes=(permissions.IsAuthenticatedOrReadOnly,)
    queryset = Food.objects.all()
    serializer_class  = FoodSerializer

    def get(self, request, pk):

        try:
            food    = Food.objects.filter(cuisine__iexact=pk)
            if not food:
                food = Food.objects.filter(category__iexact=pk)
            if not food:
                food = Food.objects.filter(name__icontains=pk)
        except:
            return Response(data={"detais":"object not found"}, status=status.HTTP_204_NO_CONTENT)
        serializer = FoodSerializer(food, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class RestaurentList(APIView):
    serializer_class  = RestaurentSerializer

    def get(self, request):
        queryset = Restaurent.objects.all()
        print(queryset)
        serializer = RestaurentSerializer(queryset, many= True,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer=RestaurentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={'details':'wrong data entered'},status=status.HTTP_400_BAD_REQUEST)
        
        
from .serializers import RestaurentSerializer

class RestaurentView(APIView):
    serializer_class = RestaurentSerializer
    def get(self, request, pk):
        try:
            queryset = Restaurent.objects.get(id=pk)
        except:
            return Response({'details':'restaurent not found with given id'})
        print(queryset)
        serializer = RestaurentSerializer(queryset)
        #if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_302_FOUND)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from cart.models import OrderItem, Cart
from cart import views
from .models import Food
from django.utils import timezone


class AddToCartOrRemove(APIView):

    def post(self, request, pk):
        item = get_object_or_404(Food, id=pk)
        #print(item,request.user)
        order_item, created = OrderItem.objects.get_or_create(item = item, user = request.user, ordered = False)
        cart_qs = Cart.objects.filter(user=request.user, ordered=False)
        #print(cart_qs)
        if cart_qs.exists():
            order = cart_qs[0]
            if order.items.filter(item__pk=item.pk).exists():
                order_item.quantity += 1
                order_item.save()
                return Response(data={'details':"item added to cart"},status=status.HTTP_201_CREATED)
            else:
                order.items.add(order_item)
                return Response(data={'details':"item added to cart"},status=status.HTTP_201_CREATED)
        else:
            ordered_date = timezone.now()
            order       = Cart.objects.create(user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            return Response(data={"details":"item added to your cart"})

    def delete(self, request, pk):
        item = get_object_or_404(Food, pk=pk )
        cart_qs = Cart.objects.filter(user=request.user, ordered=False)
        if cart_qs.exists():
            order = cart_qs[0]
            if order.items.filter(item__pk=item.pk).exists():
                order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
                order_item.delete()
                return Response(data={'details':'item removed from your cart'})
            else:
               return Response(data= {'details':"item doesn't exists"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'details':"you don't have any order"},status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        item = get_object_or_404(Food, pk=pk)
        order_qs = Cart.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__pk=item.pk).exists():
                order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
                if order_item.quantity>1:
                    order_item.quantity -=1
                    order_item.save()
                else:
                    order_item.delete()
                return Response(data={"details":"Food Item quantity updated"}, status= status.HTTP_200_OK)
            else:
                return Response(data={"details":"Food Item does not exists"}, status=status.HTTP_410_GONE)
        return Response(data={"details":"You do not have an order"}, status=status.HTTP_404_NOT_FOUND)
