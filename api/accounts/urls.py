from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from accounts import views
from django.urls import path
from rest_framework_simplejwt import views as jwt_views


router = routers.DefaultRouter()
router.register('signup', views.CreateUserAccount)
#router.register('forgotpassword', views.ChangePassword)

urlpatterns = [
    # url(r'^createaccount/$',  CreateUserAccount.as_view(),  name="createaccount"),
    url(r'^', include(router.urls)),
    path('accounts/', views.UserAccountsList.as_view()),
    path('accounts/<int:id>/', views.UserAccountsDetails.as_view()),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # path('changepassword/', views.ChangePassword.as_view()),
    # path('otp/', GenerateOTP.as_view()),
    path('verify_otp/',  views.VerifyOTP.as_view()),
    #path('signup/',  CreateUserAccount.as_view(), name='sign_up'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

router = routers.SimpleRouter()
router.register(r'foodlist', views.FoodList)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
    url(r'^', include(router.urls)),
]


