from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework import urls as resturls
from accounts import views
from django.urls import path
from rest_framework_simplejwt import views as jwt_views



app_name = 'accounts'

#url patterns for authentication

urlpatterns = [
    path('api/signup/',  views.CreateUserAccount.as_view(),  name="createaccount"),
    path('api/accounts/', views.UserAccountsDetails.as_view()),
    path('api/updateaccount/<id>/', views.UserAccountUpdate.as_view()),
    path('api/otp_verified/', views.CheckOTPVerifiedStatus.as_view(), name='ifverified'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_view'),
    path('api/resetpassword/', views.ForgotPassword.as_view()),
    path('api/passresetotp/', views.ResetPasswordOTP.as_view()),
    path('api/otp/', views.GenerateOTP.as_view()),
    path('api/verify_otp/',  views.VerifyOTP.as_view()),
    #path('api/accounts/', views.UserAccountsList.as_view()),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#fooditems related urlpatterns

# router = routers.DefaultRouter()
# router.register(r'restaurent', views.RestaurentList)

urlpatterns += [
    path('api/foodlist/', views.FoodList.as_view()),
    #path('api/foodlist/<pk>/', views.FoodList.as_view()),
    path('api/foodlist/<pk>/', views.FoodView.as_view(), name='food-detail'),
    path('api/addfood/', views.AddFoodItem.as_view(), name='add-food-detail'),
    path('api/restaurentlist/', views.RestaurentList.as_view(), name='restaurent-detail'),
    path('api/restaurent/<int:pk>/', views.RestaurentView.as_view()),
]
urlpatterns += [
    path('api/add-to-cart/<pk>/', views.AddToCartOrRemove.as_view(), name='add-to-cart'),
    # path('api/api-auth/', include(resturls)),
    #url(r'^', include(router.urls)),
]