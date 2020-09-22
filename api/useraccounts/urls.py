from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from useraccounts.views import UserViewSet

from django.urls import path


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

