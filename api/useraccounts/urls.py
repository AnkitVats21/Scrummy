from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from useraccounts.views import UserAccountsList, UserAccountsDetails, GenerateOTP

from django.urls import path


# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    
    path('accounts/', UserAccountsList.as_view()),
    path('accounts/<int:id>/', UserAccountsDetails.as_view()),

    # path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # path('otp/', OtpCreation.as_view()),
    
    path('otp/', GenerateOTP.as_view()),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

