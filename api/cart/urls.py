from cart import views
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers


# router = routers.DefaultRouter()
# router.register('order', OrderItemView)
# router.register('order', OrderView)

urlpatterns = [
    path('cart/', views.CartView.as_view()),
    path('orderitems/<id>/', views.OrderItemView.as_view()),
    path('orderitems/', views.OrderItemListView.as_view()),
    path('checkoutaddress/', views.CheckoutView.as_view()),
    path('myorders/', views.MyOrderListView.as_view()),
 ]
