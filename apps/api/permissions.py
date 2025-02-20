from rest_framework import permissions


class IsTaskOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.assign_to == request.user or request.user.is_staff
