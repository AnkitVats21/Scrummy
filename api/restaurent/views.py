from django.shortcuts import render
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import permissions, viewsets, status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from cart.models import Cart, OrderItem, CheckoutAddress, Payment
from cart.serializers import CartSerializer, OrderItemSerializer, MyOrderSerializer, CheckoutAddressSerializer, PaymentSerializer
from accounts.serializers import FoodSerializer
from accounts.models import Food, User,Restaurent
from cart.models import OrderItem, MyOrder
from .serializers import EmployeeSerializer, FeedbackSerializer
from .models import Employee, Revenue, Feedback
from .permissions import IsRestaurentOwner
from django.template.loader import render_to_string

class RestaurentOrderView(APIView):
    permission_classes = (permissions.IsAuthenticated,IsRestaurentOwner,)
    def get(self,request,pk):##pk==id showall/pk==id undelivered/pk==id delivered #id is rest_id action{showall,undelivered,delivered}
        rest_id,action      =   pk.split()
        if action=='showall':
            ordered_food    = MyOrder.objects.filter(ordered=True).filter(restaurant=rest_id)
            serializer      = MyOrderSerializer(ordered_food, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if action=='undelivered':
            ordered_food    = MyOrder.objects.filter(ordered=True,delivery_status=False).filter(restaurant=rest_id)
            serializer      = MyOrderSerializer(ordered_food, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if action=='delivered':
            ordered_food    = MyOrder.objects.filter(ordered=True,delivery_status=True).filter(restaurant=rest_id)
            serializer      = MyOrderSerializer(ordered_food, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self,request,pk):
        rest_id,order_id    = pk.split()
        ordered_food        = MyOrder.objects.filter(delivery_status=False).filter(restaurant=ffr.id)
        food=ordered_food.filter(id=pk)
        food.delivery_status==True
        food.save()
        #context      = {'':}
        # html_message = render_to_string('otp_template.html', context)
        # head         = ''
        # body         = ''
        # send_mail(head, str(body), 'in.scrummy@gmail.com', [user_email], html_message = html_message)
        return Response({"details":"Item delivered"})

class EmployeeRelatedView(viewsets.ModelViewSet):
    permission_classes  = (permissions.IsAuthenticated, IsRestaurentOwner,)
    serializer_class    = EmployeeSerializer
    queryset            = Employee.objects.all()

# class EmployeeTaskView(APIView):
#     permission_classes  = (permissions.IsAuthenticated, IsRestaurentOwner)

#     def get(self, request):

from cart.models import Payment
from cart.serializers import PaymentSerializer

class PaymentsView(APIView):
    permission_classes  = (permissions.IsAuthenticated, IsRestaurentOwner,)
    def get(self, request, pk):
        if pk=="totalsale":
            try:
                rest        = Restaurent.objects.filter(user=request.user)
            except:
                return Response({"details":"Apke koi restaurent nhi hai."})
            total_pay = {}
            total=0
            for i in range(len(rest)):
                ir      = rest[i].id
                name    = rest[i].restaurent_name
                data    = Payment.objects.filter(restaurant=ir)
                p=0
                for j in range(len(data)):
                    p       += int(data[j].amount)
                total_pay[name]=p
                total += p
            total_pay['total']=total
            return Response(total_pay, status=status.HTTP_200_OK)

        try:
            rest        = Restaurent.objects.filter(user=request.user).filter(id=pk)[0]
        except:
            return Response({"details":"Ye apka restaurent nhi hai."})
        data        = Payment.objects.filter(restaurant=rest.id)
        serializer  = PaymentSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FeedbackView(APIView):
    #permission_classes = (permissions.IsAuthenticated,)
    serializer_class= FeedbackSerializer
    def get(self, request, pk):
        if pk == 'total':
            obj     = Feedback.objects.all()
            total   = 0
            one     = 0
            two     = 0
            three   = 0
            four    = 0
            five    = 0
            for i in range(len(obj)):
                rate    = obj[i]
                total  += rate.rate_count
                if rate.rate_count == 1:
                    one +=1
                if rate.rate_count == 2:
                    two +=1
                if rate.rate_count == 3:
                    three +=1
                if rate.rate_count == 4:
                    four +=1
                if rate.rate_count == 5:
                    five +=1
            total = total/(one+two+three+four+five)
            data = {
                "total":total,
                "one":one,
                "two":two,
                "three":three,
                "four":four,
                "five":five,
            }
            return Response(data=data,status=status.HTTP_200_OK)

        if pk=='show':
            try:
                obj = Feedback.objects.filter(user=request.user)[0]
            except:
                return Response(data={"details":"user not found"},status=status.HTTP_400_BAD_REQUEST)
            serializer = FeedbackSerializer(obj)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({"details":"invalid request"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        if pk=='addreview':
            try:
                obj = Feedback.objects.filter(user=request.user)[0]
                return Response({"details":"You have already reviewed. Try to edit."})
            except:
                return Response(data={"details":"user not found"},status=status.HTTP_400_BAD_REQUEST)
            request.data["user"]=request.user.id
            serializer = FeedbackSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"details":"invalid request"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        if pk=='editreview':
            try:
                obj = Feedback.objects.filter(user=request.user)[0]
            except:
                return Response(data={"details":"user not found"},status=status.HTTP_400_BAD_REQUEST)
            request.data["user"]=request.user.id
            serializer = FeedbackSerializer(data=request.data)
            if serializer.is_valid():
                obj.rate_count=request.data.get("rate_count")
                obj.review=request.data.get("review")
                obj.save()
                return Response(FeedbackSerializer(obj).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"details":"invalid request"}, status=status.HTTP_400_BAD_REQUEST)