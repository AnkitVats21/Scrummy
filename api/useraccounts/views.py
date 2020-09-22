from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser

from .models import User
from .serializers import UserSerializer


from random import randint
from django.core.mail import send_mail


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


