import time
from rest_framework import viewsets, status, generics, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import User, OTP, Food, Restaurent
from .serializers import UserSerializer, OTPSerializer, FoodSerializer, RestaurantSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from random import randint
from django.core.mail import send_mail
from django.http import Http404
from restaurent.permissions import IsRestaurentOwner
from django.template.loader import render_to_string
from django.shortcuts import render

class VerifyOTP(APIView):
    queryset            = OTP.objects.all()
    serializer_class    = OTPSerializer

    def post(self, request):
        request_data = request.data
        request_otp  = request_data.get("otp", "")
        request_email= request_data.get("otp_email", "")
        t1           = int(time.time())
        
        try:
            obj     = OTP.objects.filter(otp_email__iexact = request_email)[0]
        except:
            data    = {"error":"OTP object not found"}
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
                    otp  = randint(100000, 999999) 
                    t    = int(time.time())
                    OTP.objects.create(otp = otp, otp_email = user_email, time= t)
                    context      = {'otp':otp}
                    #return render(request,'otp_template.html',context)
                    html_message = render_to_string('otp_template.html', context)
                    head         = 'OTP Verification'
                    body = ("Your One Time Password is {} for registration on Scrummy.").format(otp)
                    send_mail(head, str(body), 'in.scrummy@gmail.com', [user_email], html_message = html_message)
                    serializer = UserSerializer(data = req_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status = status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                    data    = {"details":"OTP sent successfully"}
                    return Response(data, status = status.HTTP_200_OK)
        else:
            data = {"error":"Please enter valid email"}
            return Response(data, status = status.HTTP_400_BAD_REQUEST)

class ResetPasswordOTP(APIView):
    def post(self, request):
        user_email  = request.data.get("email")
        request_otp = request.data.get("otp")
        #print(user_email,request_otp)
        #user = User.objects.filter(email__iexact = user_email)[0]
        try:
            obj = OTP.objects.filter(otp_email__iexact = user_email)[0]
        except:
            data= {"error":"wrong email"}
            return Response(data,status=status.HTTP_404_NOT_FOUND)
        t1  = time.time()
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
        #print(request_email, "pass:", request_password)
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
            raise Http404
        
    def get(self, request):
        user_id=request.user.id
        #print(user_id)
        user = self.get_object(id=str(user_id))
        serializer = UserSerializer(user)
        return Response(serializer.data)
        # return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserAccountUpdate(APIView):
    permission_classes  = (permissions.IsAuthenticated,)
    serializer_class    = UserSerializer
    def patch(self, request,id):
        user_id=request.user.id
        user = User.objects.filter(id=id)
        serializer = UserSerializer(request.user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user_id=request.user.id
        user = User.objects.get(id=id)# self.get_object(id)
        user.delete()
        return Response(data={"details":"account deleted"},status = status.HTTP_204_NO_CONTENT)


    
class GenerateOTP(APIView):
    def post(self, request):
        user_email = request.data.get("email")

        try:
            user   = User.objects.filter(email__iexact = user_email)[0]
        except:
            return Response(data={"error":"User not found with given email"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            obj    = OTP.objects.filter(otp_email__iexact = user_email)[0]
            obj.delete()
        except:
            if check(user_email):
                t=int(time.time())
                otp     = randint(1000, 9999) 
                body    = ("Hello! Your OTP is {}. Do not share it with anyone.").format(otp)
                OTP.objects.create(otp = otp, otp_email = user_email, time =t)
                send_mail('OTP Verification', body, 'in.scrummy@gmail.com', [user_email], fail_silently = False)
                return Response(data = {"details":"OTP sent succesfully"}, status = status.HTTP_200_OK)
            else:
                return Response(data = { "error":"invalid email"}, status = status.HTTP_406_NOT_ACCEPTABLE)

        if check(user_email):
            t=int(time.time())
            otp     = randint(1000, 9999) 
            body    = ("Hello! Your OTP is {}. Do not share it with anyone.").format(otp)
            OTP.objects.create(otp = otp, otp_email = user_email, time =t)
            send_mail('OTP Verification', body, 'in.scrummy@gmail.com', [user_email], fail_silently = False)
            return Response(data = {"details":"OTP sent succesfully"}, status = status.HTTP_200_OK)
        else:
            return Response(data = { "error":"invalid email"}, status = status.HTTP_406_NOT_ACCEPTABLE)
        
class CheckOTPVerifiedStatus(APIView):
    def post(self , request, **args):
        request_email       = request.data.get('email')
        request_password    = request.data.get('password')
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
        data=food[0]
        data= data.rest_food
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        food_data   = request.data
        user_email  = request.user
        user        = User.objects.filter(email__iexact=str(user_email))
        if user.restaurent:
            serializer = FoodSerializer(data=food_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(data={"details":"please enter valid data"})
        return Response(data={"details":"you are not a provider"})
        

class FoodView(APIView):
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)
    queryset = Food.objects.all()
    serializer_class  = FoodSerializer

    def get(self, request, pk):

        try:
            restaurent_name = Restaurent.objects.filter(restaurent_name__iexact=pk)
            rest_id         = restaurent_name[0].id
            food            = Food.objects.filter(rest_food=int(rest_id))
            serializer      = FoodSerializer(food, many=True, context={'request':request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            pass
        try:
            food    = Food.objects.filter(cuisine__iexact=pk)
            if not food:
                food = Food.objects.filter(category__istartswith=pk)
            if not food:
                food = Food.objects.filter(name__icontains=pk)
            if not food:
                food = Food.objects.filter(id=pk)
        except:
            return Response(data={"detais":"object not found"}, status=status.HTTP_204_NO_CONTENT)
        serializer = FoodSerializer(food, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)



from cart.models import OrderItem, Cart
from cart import views
from .models import Food
from django.utils import timezone


class AddToCartOrRemove(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        item    = get_object_or_404(Food, id=pk)
        order_item, created = OrderItem.objects.get_or_create(restaurant=item.rest_food, item = item, user = request.user, ordered = True)
        cart_qs = Cart.objects.filter(user=request.user, ordered=False)
        if cart_qs.exists():
            order = cart_qs[0]
            if order.items.filter(item__pk=item.pk).exists():
                order_item.quantity += 1
                order_item.save()
                data = ("item quantity increased to {} in the cart.").format(order_item.quantity)
                return Response(data={"details":data,"quantity":order_item.quantity},status=status.HTTP_201_CREATED)
            else:
                order.items.add(order_item)
                return Response(data={'details':"item added to cart"},status=status.HTTP_201_CREATED)
        else:
            ordered_date = timezone.now()
            order        = Cart.objects.create(user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            return Response(data={"details":"item added to your cart"},status=status.HTTP_201_CREATED)


    def post(self, request, pk):
        item = get_object_or_404(Food, id=pk)
        prevOrder   = OrderItem.objects.filter(user=request.user).filter(ordered=True)
        order_item, created = OrderItem.objects.get_or_create(restaurant=item.rest_food, item = item, user = request.user, ordered = True)
        if len(prevOrder)==0 : #by pass wishlist by adding <or len(prevOrder)!=0>
            #order_item, created = OrderItem.objects.get_or_create(restaurant=item.rest_food, item = item, user = request.user, ordered = True)
            cart_qs = Cart.objects.filter(user=request.user, ordered=False)
            if cart_qs.exists():
                order = cart_qs[0]
                order.items.add(order_item)
                return Response(data={'details':"item added to cart"},status=status.HTTP_201_CREATED)
            else:
                ordered_date = timezone.now()
                order       = Cart.objects.create(user=request.user, ordered_date=ordered_date)
                order.items.add(order_item)
                return Response(data={"details":"item added to your cart"})

        try:
            if request.data.get('action')=='move to wishlist':
                cart_qs = Cart.objects.filter(user=request.user, ordered=False)
                if cart_qs.exists():
                    order = cart_qs[0]
                    if order.items.filter(item__pk=item.pk).exists():
                        order_item.ordered = False
                        order_item.save()
                        return Response(data={'details':"item moved to wishlist"},status=status.HTTP_201_CREATED)
                    else:
                        order_item.ordered = False
                        order_item.save()
                        order.items.add(order_item)
                        return Response(data={'details':"item moved to wishlist"},status=status.HTTP_410_GONE)
                    return Response({"error":"unexpected error"})
            if request.data.get('action')=='add to cart':
                cart_qs = Cart.objects.filter(user=request.user, ordered=False)
                if cart_qs.exists():
                    order = cart_qs[0]
                    if order.items.filter(item__pk=item.pk).exists():
                        for i in range(len(prevOrder)):
                            item=prevOrder[i]
                            print(item)
                            item.ordered=False
                            item.save()
                        order_item.ordered = True
                        order_item.save()
                        return Response(data={'details':"item added to your cart and previous one moved to wish list"},status=status.HTTP_201_CREATED)
                    else:
                        for i in range(len(prevOrder)):
                            item=prevOrder[i]
                            print(item)
                            item.ordered=False
                            item.save()
                        order_item.ordered = True
                        order_item.save()
                        order.items.add(order_item)
                        return Response(data={'details':"item added to your cart and previous one moved to wish list"},status=status.HTTP_201_CREATED)
                    return Response({"error":"unexpected error"})
        except:
            pass

        if prevOrder[0].restaurant==item.rest_food:
            order_item, created = OrderItem.objects.get_or_create(restaurant=item.rest_food, item = item, user = request.user, ordered = True)
            cart_qs = Cart.objects.filter(user=request.user, ordered=False)
            if cart_qs.exists():
                order = cart_qs[0]
                if order.items.filter(item__pk=item.pk).exists():
                    return Response(data={'details':"item already in your cart"},status=status.HTTP_201_CREATED)
                else:
                    order.items.add(order_item)
                    print(order_item)
                    return Response(data={'details':"item added to cart"},status=status.HTTP_201_CREATED)
            else:
                ordered_date = timezone.now()
                order       = Cart.objects.create(user=request.user, ordered_date=ordered_date)
                order.items.add(order_item)
                print(order_item)
                return Response(data={"details":"item added to your cart"})
        return Response(data={"details":"conflicting restaurant"})

############api--> api/cart/clearcart/   {'with delete request'}  <-- for removing all items from cart#############

    def delete(self, request, pk):
        if pk == 'clearcart':
            id1     =request.user.id
            try:
                orders  = OrderItem.objects.filter(user=id1)
                orders.delete()
                return Response(data={"details":"your cart has been cleared"}, status=status.HTTP_404_NOT_FOUND)
            except:
                raise Http404

        item = get_object_or_404(Food, pk=pk )
        cart_qs = Cart.objects.filter(user=request.user, ordered=False)
        if cart_qs.exists():
            order = cart_qs[0]
            if order.items.filter(item__pk=item.pk).exists():
                order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=True)[0]
                #print(order_item)
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
                order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=True)[0]
                if order_item.quantity>1:
                    order_item.quantity -=1
                    order_item.save()
                else:
                    order_item.delete()
                data = ("item quantity decreased to {} in the cart.").format(order_item.quantity)
                return Response(data={"details":data,"quantity":order_item.quantity},status=status.HTTP_201_CREATED)
                #return Response(data={"details":"Food Item quantity updated"}, status= status.HTTP_200_OK)
            else:
                return Response(data={"details":"Food Item does not exists"}, status=status.HTTP_410_GONE)
        return Response(data={"details":"You do not have an order"}, status=status.HTTP_404_NOT_FOUND)
########################rating function########################
    def put(self,request,pk):
        item = get_object_or_404(Food, pk=pk)
        rating = request.data.get("rating")
        print(rating)
        a=item.rating
        b=a.split()
        # if pk[1:]=="editreview":
        #     previous_rating=request.data.get("prev_rating")
        #     x=int(b[0])+int(rating)-int(previous_rating)
        #     y=int(b[1])
        #     data=x/y
        #     a=str(x)+" "+str(y)
        #     item.rating=a
        #     item.save()
        #     return Response(data={"rating":data},status=status.HTTP_202_ACCEPTED)
        x=int(b[0])+int(rating)
        y=int(b[1])+1
        data=x/y
        a=str(x)+" "+str(y)
        item.rating=a
        item.save()
        return Response(data={"rating":data},status=status.HTTP_202_ACCEPTED)

######################################
#   """"""""""""""""""""""""""""     #
#   add food item in restaurent      #
#   """"""""""""""""""""""""""""     #
######################################

class RestaurantList(APIView):
    serializer_class  = RestaurantSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        #id1=request.user.id
        try:
            queryset = Restaurent.objects.all()#filter(user=id1)
        except:
            raise Http404
        serializer = RestaurantSerializer(queryset, many= True,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        id1=request.user.id
        data = request.data
        try:
            user = User.objects.filter(id=id1)[0]
        except:
            raise Http404
        if user.restaurent:
            serializer=RestaurantSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={'details':'user is not restaurent owner'},status=status.HTTP_400_BAD_REQUEST)
   
        
from .serializers import RestaurantSerializer

class RestaurantView(APIView):
    serializer_class = RestaurantSerializer
    def get(self, request, pk):
        try:
            queryset = Restaurent.objects.get(id=pk)
        except:
            return Response({'details':'restaurent not found with given id'})
        serializer = RestaurantSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
########__--->>>>>>>>>>>Restaurant rating<<<<<<<<<<<<---__########
    def put(self,request,pk):
        #id1         =   request.data.get("id")
        rating       =   request.data.get("rating")
        restaurant  =   get_object_or_404(Restaurent,id=pk)
        a=restaurant.rating
        b=a.split()
        x=int(b[0])+int(rating)
        y=int(b[1])+1
        data=x/y
        a=str(x)+" "+str(y)
        restaurant.rating=a
        restaurant.save()
        return Response(data={"rating":data},status=status.HTTP_202_ACCEPTED)


class AddFoodItem(APIView):
    serializer_class    = FoodSerializer
    permission_classes  = (permissions.IsAuthenticated,IsRestaurentOwner)
    def post(self, request):
        id1=request.user.id
        try:
            user    = User.objects.get(id=id1)
        except:
            raise Http404
        serializer  = FoodSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)