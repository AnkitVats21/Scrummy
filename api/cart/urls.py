from cart import views
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

urlpatterns = [
    path('api/cart/<pk>/', views.OrderItemView.as_view()), #if pk=='ordered' my order view will be shown 
    path('api/checkoutaddress/', views.CheckoutAddressView.as_view()),
    path('api/payment/', views.PaymentView.as_view()),
    path('api/orderstatus/<pk>/', views.CheckOrderStatus.as_view()),
    path('cart/<pk>/', views.CartView.as_view()),
    #path('orderitemslist/', views.OrderItemListView.as_view()),
 ]
