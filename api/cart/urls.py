from .views import OrderItemView, OrderView
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers


# router = routers.DefaultRouter()
# router.register('order', OrderItemView)
# router.register('order', OrderView)

urlpatterns = [
    path('order/', OrderView.as_view()),
    path('orderitems/', OrderItemView.as_view()),
 ]
