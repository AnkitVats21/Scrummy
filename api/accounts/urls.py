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
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#fooditems related urlpatterns

urlpatterns += [
    path('api/foodlist/', views.FoodList.as_view()),
    path('api/foodlist/<pk>/', views.FoodView.as_view(), name='food-detail'),
    path('api/addfood/', views.AddFoodItem.as_view(), name='add-food-detail'),
    path('api/restaurantlist/', views.RestaurantList.as_view(), name='restaurent-detail'),
    path('api/restaurant/<pk>/', views.RestaurantView.as_view()),
    path('api/add-to-cart/<pk>/', views.AddToCartOrRemove.as_view(), name='add-to-cart'),
    #add-to-cart/<pk>/ here pk is id of the food
    #in request if you pass {"action":"move to wishlist"} then that food item will be added to wish list
    #but if you'll pass {"action":"add to cart"} then previous orders will be moved to wishlist and new one will be added to cart
    #and if you'll pass nothing then simple functionalities wil be called 
]
# urlpatterns += [
#     # path('api/api-auth/', include(resturls)),
#     #url(r'^', include(router.urls)),
# ]