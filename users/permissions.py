from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status


class OnlyAdminPermission(BasePermission):
    def has_permission(self, request, view):

        if request.method == 'POST':
            return True

        if request.user.is_authenticated and request.user.is_admin == True:
            return True

        return False


class TokenRecoveryPermission(BasePermission):

    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            return Response({'message': 'Invalid code for recovery'}, status=status.HTTP_400_BAD_REQUEST)
        
        return True