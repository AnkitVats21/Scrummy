from cart import views
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers


# router = routers.DefaultRouter()
# router.register('order', OrderItemView)
# router.register('order', OrderView)

urlpatterns = [
    path('cart/<pk>/', views.CartView.as_view()),
    path('api/cart/', views.OrderItemView.as_view()),
    path('orderitemslist/', views.OrderItemListView.as_view()),
    path('checkoutaddress/', views.CheckoutView.as_view())
 ]
