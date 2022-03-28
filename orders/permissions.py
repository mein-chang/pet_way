from rest_framework.permissions import BasePermission


class IsCustomerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_admin == False and request.user.is_provider == False:
            return True

        if request.user.is_admin == True and request.method == 'GET':
            return True


class IsProviderAccount(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user.id == request.user.id:
            return True

        return False
