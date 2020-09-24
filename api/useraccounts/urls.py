from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from useraccounts.views import UserAccountsList, UserAccountsDetails, GenerateOTP, VerifyOTP, CreateUserAccount

from django.urls import path
from rest_framework_simplejwt import views as jwt_views


# router = routers.DefaultRouter()
# router.register('users', CreateUserAccount)

urlpatterns = [
    url(r'^createaccount/$',  CreateUserAccount.as_view(),  name="createaccount"),
    #url(r'^', include(router.urls)),
    path('accounts/', UserAccountsList.as_view()),
    path('accounts/<int:id>/', UserAccountsDetails.as_view()),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    
    path('otp/', GenerateOTP.as_view()),
    path('verify_otp/',  VerifyOTP.as_view()),
    #path('createaccount/',  CreateUserAccount.as_view()),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

