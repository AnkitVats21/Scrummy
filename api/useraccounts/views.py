import time
from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import User, OTP
from .serializers import UserSerializer, OTPSerializer
#from .permissions import UserPermission, UserDetailPermissions

from random import randint
from django.core.mail import send_mail


class VerifyOTP(generics.CreateAPIView):
    #otp = OTP.objects.all()
    serializer_class = OTPSerializer

    def post(self, request):

        request_data = request.data
        request_otp  = request_data.get("otp", "")
        request_email= request_data.get("otp_email", "")
        t1           = int(time.time())
        print(request_email,request_otp)
        try:
            obj = OTP.objects.filter(otp_email__iexact = request_email)[0]
        except:
            data = {"details":"OTP object not found"}
            return Response(data,status=status.HTTP_404_NOT_FOUND)

        stored_db_email  = obj.otp_email 
        stored_db_otp    = obj.otp
        t2               = obj.time

        if (t1-t2)>30000:
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

class CreateUserAccount(generics.CreateAPIView):
    serializer_class = UserSerializer
    


            

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
            body = ("Hello! Your one time password verification for registering in Scrummy is {}").format(otp)
            OTP.objects.create(otp = otp, otp_email = user_email, time =t)
            send_mail('OTP Verification', body, 'in.scrummy@gmail.com', [user_email], fail_silently = False)
            return Response(status = status.HTTP_200_OK)
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