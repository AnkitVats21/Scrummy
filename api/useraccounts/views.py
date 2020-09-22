from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser

from .models import User, OTP
from .serializers import UserSerializer


from random import randint
from django.core.mail import send_mail


class UserAccountsList(APIView):

    def get(self, request):
        users       = User.objects.all()
        serializer  = UserSerializer(users, many = True)
        return Response(serializer.data)

    def post(self, request):

        request_data = request.data
        request_otp  = request_data.get("otp", "")
        request_email= request_data.get("email", "")
        
        try:
            obj = OTP.objects.filter(otp_email__iexact = request_email)[0]
            
        except:
            
            return Response(status=status.HTTP_404_NOT_FOUND)

        stored_db_email  = obj.otp_email 
        stored_db_otp    = obj.otp
        print(obj)
        print(request_email,stored_db_email," ",stored_db_otp,request_otp)
        if stored_db_email == request_email and stored_db_otp == request_otp:
            serializer = UserSerializer(data = request_data)
            if serializer.is_valid():
                serializer.save()
                obj.delete()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_400_BAD_REQUEST)
            

class UserAccountsDetails(APIView):

    def get_object(self, id):
        try:
            return User.objects.get(id = id)
        except User.DoesNotExist:
            raise Http404 
    
    def get(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = self.get_object(id)
        user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)



    

    

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == 'create':
    #         permission_classes = [AllowAny]
    #     elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         permission_classes = [IsLoggedInUserOrAdmin]
    #     elif self.action == 'list' or self.action == 'destroy':
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]


class GenerateOTP(APIView):
    def post(self, request):
        user_email = request.data.get("email", "")
        if user_email:
            user = User.objects.filter(email__iexact = user_email)
            
            if user.exists():
                    return Response(status = status.HTTP_406_NOT_ACCEPTABLE)
            else:
                    otp = randint(1000, 9999) 
                    body = ("Hello! Your one time password verification for registering in Scrummy is {}").format(otp)
                    OTP.objects.create(otp = otp, otp_email = user_email)
                    send_mail('OTP Verification', body, 'in.scrummy@gmail.com', [user_email], fail_silently = False)
                    return Response(status = status.HTTP_200_OK)
        
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST) 

        