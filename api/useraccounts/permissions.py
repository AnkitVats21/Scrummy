# # from rest_framework import permissions

# # class IsLoggedInUserOrAdmin(permissions.BasePermission):
    
# #     def has_object_permission(self, request, view, obj):
# #         return obj == request.user or request.user.is_staff

# # class IsAdminUser(permissions.BasePermission):

# #     def has_permission(self, request, view):
# #         return request.user and request.user.is_staff

# #     def has_object_permission(self, request, view, obj):
# #         return request.user and request.user.is_staff

# #from rest_framework.permissions import BasePermission

# # class PostOnlyPermissions(BasePermission):
# #     def has_permission(self, request, view):
# #         print("cfiwebci testing self.actions")
# #         if self.action in ('create', ): # for POST method the action in DRF is create
# #             return True
# #         return False

# from rest_framework import permissions

# class UserPermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.method == 'GET':
#             if request.user.is_superuser:
#                 return True
#         elif request.method == 'POST':
#             return True
#         # elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
#         #     return True
#         # else:
#         #     return False

#     def has_object_permission(self, request, view, obj):
#         # Deny actions on objects if the user is not authenticated
#         if not request.user.is_authenticated():
#             return False

#         if view.action == 'retrieve':
#             return obj == request.user or request.user.is_admin
#         elif view.action in ['update', 'partial_update']:
#             return obj == request.user or request.user.is_admin
#         elif view.action == 'destroy':
#             return request.user.is_admin
#         else:
#             return False

# class UserDetailPermissions(permissions.BasePermission):

#     def has_permission(self, request, view):
#         #print(request.user.id==id.id)
#         if request.method == 'GET':
#             if request.user.is_superuser:
#                 return True
#         elif request.user.is_authenticated:
#             return True