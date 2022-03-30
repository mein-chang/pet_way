from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsClientOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_provider == False and request.user.is_admin == False:
            return True

        return False
    
    
class IsOwnerPet(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user.id == request.user.id:
            return True
        
        return False