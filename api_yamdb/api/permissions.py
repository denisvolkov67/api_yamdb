from rest_framework import permissions 
from reviews.models import UserRole
 
class IsAdmin(permissions.BasePermission): 
 
    def has_permission(self, request, view):
        return request.user.role == UserRole.ADMIN or request.user.is_superuser

    def has_object_permission(self, request, view, obj): 
        return request.user.role == UserRole.ADMIN or request.user.is_superuser


class IsMeUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj): 
        return request.user == obj