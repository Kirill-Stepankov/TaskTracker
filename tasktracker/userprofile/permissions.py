from rest_framework import permissions


class IsAnonymous(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated
    
class IsAdminOrIsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff) or obj == request.user
    
class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user

