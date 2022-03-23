from rest_framework.permissions import BasePermission


class OnlyAdminPermission(BasePermission):
    def has_permission(self, request, view):

        if request.method == 'POST':
            return True

        if request.user.is_admin == True:
            return True

        return False