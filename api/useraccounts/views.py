import time
from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import User, OTP, Food, Restaurent
from .serializers import UserSerializer, OTPSerializer, FoodSerializer, RestaurentSerializer
#from .permissions import UserPermission, UserDetailPermissions

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
            data = {"details":"OTP object not found"}
            return Response(data,status=status.HTTP_404_NOT_FOUND)

        stored_db_email  = obj.otp_email 
        stored_db_otp    = obj.otp
        t2               = obj.time

        if (t1-t2)>5000:
            obj.delete()
            data = {"details":"otp expired"}
            return Response(data,status = status.HTTP_404_NOT_FOUND)
        elif stored_db_email == request_email and stored_db_otp == request_otp:
            data = {"details":"otp verified"}
            user = User.objects.filter(email__iexact = request_email)[0]
            try:
                user = User.objects.filter(email__iexact = request_email)[0]
            except:
                data = {"details":"email not found in users"}
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            obj.delete()
            user.is_active=True
            user.save()
            return Response(data , status = status.HTTP_200_OK)
        return Response(status = status.HTTP_404_NOT_FOUND)
        


class UserAccountsList(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        users       = User.objects.all()
        serializer  = UserSerializer(users, many = True)
        return Response(serializer.data)

class CreateUserAccount(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request):
        user_email  = request.data.get("email")
        req_data    =request.data
        if check(user_email):
            user = User.objects.filter(email__iexact = user_email)
            
            if user.exists():
                data = {"details":"User with the given email address already exists"}
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
            data = {"details":"Please enyer valid email"}
            return Response(data, status = status.HTTP_400_BAD_REQUEST)
        # if serializer.is_valid():
        #     serializer.save()
        # else:
        #     print("nahi save hua")
        # if check(user_email):
        #     t=int(time.time())
        #     otp = randint(1000, 9999) 
        #     body = ("Hello! Your one time password verification for registering in Scrummy is {}").format(otp)
        #     #OTP.objects.create(otp = otp, otp_email = user_email, time =t)
        #     #send_mail('OTP Verification', body, 'in.scrummy@gmail.com', [user_email], fail_silently = False)
        #     data = { "details":"OTP Sent"}
        #     return Response(data, status = status.HTTP_200_OK)
        # else:
        #     data = { "details":"invalid email"}
        #     return Response( data, status = status.HTTP_406_NOT_ACCEPTABLE)
        # # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ChangePassword(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def put(self, request):
        request_email       = request.get('email')
        request_password    = request.get('password')
        print(request_email,request_password)
        user = self.get_object(email=request_email)
        t1= int(time.time())
        try:
            obj = OTP.objects.filter(otp_email__iexact = request_email)[0]
        except:
            data = {"details":"OTP object not found"}
            return Response(data,status=status.HTTP_404_NOT_FOUND)
        stored_db_email  = obj.otp_email 
        stored_db_otp    = obj.otp
        t2               = obj.time

        if (t1-t2)>10000:
            obj.delete()
            data = {"details":"otp expired"}
            return Response(data,status = status.HTTP_404_NOT_FOUND)
        if stored_db_otp == request_otp:
            serializer = UserSerializer(user, data = request_password)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_200_OK)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            data={"details":"Invalid OTP"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


        # try:
        #     user = User.objects.filter(email__iexact = request_email)[0]
        # except:
        #     data = {"details":"User not found with this email"}
        #     return Response(data, status = status.HTTP_404_NOT_FOUND)
        
        # t1= int(time.time())
        # try:
        #     obj = OTP.objects.filter(otp_email__iexact = request_email)[0]
        # except:
        #     data = {"details":"OTP object not found"}
        #     return Response(data,status=status.HTTP_404_NOT_FOUND)
        # stored_db_email  = obj.otp_email 
        # stored_db_otp    = obj.otp
        # t2               = obj.time

        # if (t1-t2)>10000:
        #     obj.delete()
        #     data = {"details":"otp expired"}
        #     return Response(data,status = status.HTTP_404_NOT_FOUND)
        # if stored_db_otp == request_otp:
        #     print(user)
        #     user.set_password(request_password)
        #     user.save()
        #     data = {"details":"Password changed successfully."},
        #     obj.delete()
        #     return Response(data, status = status.HTTP_200_OK)
        # else:
        #     data={"details":"Invalid OTP"}
        #     return Response(data, status=status.HTTP_400_BAD_REQUEST)

        #     user = self.get_object(email=request_email)
        #     serializer = UserSerializer(user, data = request_password)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status= status.HTTP_200_OK)
        #     return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            

class UserAccountsDetails(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, id):
        
        try:
            return User.objects.get(id = id)
        except User.DoesNotExist:
            raise Http404 
    
    def get(self, request, id):

        user_id=request.user.id
        data = {"details":"Access Denied"},
        if user_id==id:
            user = self.get_object(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response( data, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        user_id=request.user.id
        data = {"details":"Access Denied"},
        if user_id==id:
            user = self.get_object(id=id)
            serializer = UserSerializer(user, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_200_OK)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response(data, status = status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        data = {"details":"Access Denied"},
        user_id=request.user.id
        if user_id==id:
            user = self.get_object(id)
            user.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        return Response(data , status = status.HTTP_400_BAD_REQUEST)


class GenerateOTP(APIView):
    def post(self, request):
        user_email = request.data.get("email", "")
        if check(user_email):
            t=int(time.time())
            otp = randint(1000, 9999) 
            body = ("Hello! Your OTP is {}. Do not share it with anyone.").format(otp)
            OTP.objects.create(otp = otp, otp_email = user_email, time =t)
            send_mail('OTP Verification', body, 'in.scrummy@gmail.com', [user_email], fail_silently = False)
            data = {"details":"OTP sent succesfully"}
            return Response(data, status = status.HTTP_200_OK)
        else:
            data = { "details":"invalid email"}
            return Response( data, status = status.HTTP_406_NOT_ACCEPTABLE)
        


#validating email

import re 
  
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def check(email):  
    if(re.search(regex,email)):  
        return True   
    else:  
        return False


class FoodList(viewsets.ModelViewSet):
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)
    queryset = Food.objects.all()
    serializer_class  = FoodSerializer



class RestaurentList(viewsets.ModelViewSet):
    queryset = Restaurent.objects.all()
    serializer_class  = RestaurentSerializer