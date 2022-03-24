import re
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET' and not request.user.is_authenticated:
            return False

        if request.user.is_admin == True:
            return True
