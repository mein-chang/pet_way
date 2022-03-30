from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from orders.models import Order


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_provider == False and request.user.is_admin == False:
            return True


class IsCustomerOrder(BasePermission):
    def has_permission(self, request, view):
        order = get_object_or_404(Order, id=view.kwargs['order_id'])

        if request.user == order.pet.user:
            return True


class IsProvider(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_provider == True:
            return True


class IsProviderOrder(BasePermission):
    def has_permission(self, request, view):
        order = get_object_or_404(Order, id=view.kwargs['order_id'])

        if request.user == order.service.provider:
            return True
