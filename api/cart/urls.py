from cart import views
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from django.shortcuts import render
from django.template import loader 
from django.http import HttpResponse 
o_d={
            "item_name":["2"],
            "quantity":["2"],
            "price":["2"],
            "discount_price":["2"]
            }
def detail(request,):
    template = loader.get_template('email_template.html') # getting our template  
    return HttpResponse(template.render()) 

urlpatterns = [
    path('api/cart/<pk>/', views.OrderItemView.as_view()), #if pk=='ordered' my order view will be shown <pk>='checkout' for placing order 
    path('api/checkoutaddress/', views.CheckoutAddressView.as_view()),
    path('api/payment/', views.PaymentView.as_view()),
    path('api/orderstatus/<pk>/', views.CheckOrderStatus.as_view()),
    path('cart/<pk>/', views.CartView.as_view()),
    path('api/myorders/', views.MyOrderView.as_view()),
    path('api/ordersummary/', detail),
 ]