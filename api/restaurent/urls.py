from restaurent import views
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

urlpatterns = [
    path('api/restorders/<pk>', views.RestaurentOrderView.as_view()),
]
