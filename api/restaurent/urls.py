from restaurent import views
from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from .views import EmployeeRelatedView


router = routers.DefaultRouter()
router.register(r'api/employee', EmployeeRelatedView, basename='employee')

urlpatterns = [
    path('api/restorders/<pk>/', views.RestaurentOrderView.as_view()),
    path('api/restpayments/<pk>/', views.PaymentsView.as_view()),
    url(r'^', include(router.urls)),
]
