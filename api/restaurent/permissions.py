from rest_framework import permissions

class IsRestaurentOwner(permissions.BasePermission):
    def has_permission(self, request, view):
            return  request.user.restaurent == True