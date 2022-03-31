from rest_framework.permissions import BasePermission


class IsProvider(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        return request.user.is_authenticated and request.user.is_provider


class IsOwnerProvider(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        return obj.provider == request.user
