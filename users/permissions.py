from rest_framework.permissions import BasePermission

from users.exceptions import InvalidCodeError


class OnlyAdminPermission(BasePermission):
    def has_permission(self, request, view):

        if request.method == 'POST':
            return True

        if request.user.is_authenticated and request.user.is_admin == True:
            return True

        return False


class TokenRecoveryPermission(BasePermission):

    def has_permission(self, request, view):
        
        if request.user.is_authenticated == False:
            raise InvalidCodeError()

        return True