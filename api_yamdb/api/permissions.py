from rest_framework import permissions
from reviews.models import UserRole


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        # return obj.author == request.user
        return (
            request.user.role == UserRole.USER
            or request.user.role == UserRole.MODERATOR
            or request.user.role == UserRole.ADMIN
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == UserRole.USER
            
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRole.ADMIN or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.role == UserRole.ADMIN or request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
            or request.user.role == UserRole.ADMIN
        )
