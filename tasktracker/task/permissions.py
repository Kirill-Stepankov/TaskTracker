from rest_framework import permissions


class IsAdminOrIsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff) or obj.owner == request.user