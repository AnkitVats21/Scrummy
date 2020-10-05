from cart import views
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

urlpatterns = [
    path('cart/<pk>/', views.CartView.as_view()),
    path('api/cart/<pk>/', views.OrderItemView.as_view()),
    path('orderitemslist/', views.OrderItemListView.as_view()),
    path('checkoutaddress/', views.CheckoutAddressView.as_view()),
    path('payment/', views.PaymentView.as_view())
 ]
