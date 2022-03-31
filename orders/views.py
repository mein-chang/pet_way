from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .exceptions import (AddressNotFoundError, DoesNotHaveAddressError,
                         DropAddressIsRequiredError, InvalidUUIDError,
                         NotProviderAccountError, NotPetOwnerAccountError,
                         CustomerAccountError, CustomerAccountOnlyError, UpdateError)
from .models import Order
from .permissions import IsCustomerOrAdmin
from .serializers import (OrderSerializer, OrderUpdatePatchSerializer,
                          OrderUpdatePutSerializer)
from addresses.models import Address, UserAddress
from pets.models import Pet
from providers_services.exceptions import IdIsNotProvider
from providers_services.models import ProviderService
from users.models import User


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCustomerOrAdmin]

    def perform_create(self, serializer):
        try:
            pet = Pet.objects.get(id=self.request.data["pet_id"])
            service = ProviderService.objects.get(
                id=self.request.data["service_id"])
            pick_up_address = Address.objects.get(
                id=self.request.data["pick_up_address_id"])

            if service.type == 'Pet taxi':
                user_id = self.request.user.id
                drop_address_id = self.request.data['drop_address_id']
                drop_address = Address.objects.get(
                    id=self.request.data["drop_address_id"])

                if drop_address == "":
                    raise DropAddressIsRequiredError()

                if not UserAddress.objects.filter(user_id=user_id, address_id=drop_address_id).exists():
                    raise DoesNotHaveAddressError()

                serializer = serializer.save(
                    pet=pet, service=service, pick_up=pick_up_address, drop=drop_address)

            else:
                serializer = serializer.save(
                    pet=pet, service=service, pick_up=pick_up_address)

            return super().perform_create(serializer)

        except KeyError:
            raise DropAddressIsRequiredError()

        except ValidationError:
            raise InvalidUUIDError()

        except Address.DoesNotExist:
            raise AddressNotFoundError()


class OrderRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "order_id"

    def get_serializer_class(self):

        if self.request.method == "PATCH":
            return OrderUpdatePatchSerializer

        return super().get_serializer_class()


    def update(self, request, *args, **kwargs):
        try:
            order_id = self.kwargs['order_id']
            token_id = self.request.user.id

            order = get_object_or_404(Order, id=order_id)
            token_user = User.objects.get(id=token_id)
            pet = Pet.objects.get(id=str(order.pet.id))

            if pet.user != token_user:
                raise CustomerAccountOnlyError()

            if "pick_up_address_id" in self.request.data and "drop_address_id" in self.request.data:
                request.data["pick_up"] = self.request.data["pick_up_address_id"]
                request.data["drop"] = self.request.data["drop_address_id"]

            elif "pick_up_address_id" in self.request.data:
                request.data["pick_up"] = self.request.data["pick_up_address_id"]

            if "drop_address_id" in self.request.data:
                request.data["drop"] = self.request.data["drop_address_id"]

            return super().update(request, *args, **kwargs)

        except IntegrityError:
            raise UpdateError()

    def delete(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        token_id = self.request.user.id

        order = get_object_or_404(Order, id=order_id)
        token_user = User.objects.get(id=token_id)

        if not (str(token_id) == str(order.pet.user.id) or token_user.is_admin):
            raise CustomerAccountError()

        return super().delete(request, *args, **kwargs)


class OrderUpdatePutView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdatePutSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "order_id"

    def update(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        token_id = self.request.user.id

        order = get_object_or_404(Order, id=order_id)
        token_user = User.objects.get(id=token_id)
        pet = Pet.objects.get(id=str(order.pet.id))

        if pet.user != token_user:
            raise CustomerAccountOnlyError()

        return super().update(request, *args, **kwargs)


class OrderListByPet(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "pet_id"

    def get_queryset(self):
        pet_id = self.kwargs['pet_id']
        token_id = self.request.user.id

        pet = get_object_or_404(Pet, id=pet_id)
        token_user = User.objects.get(id=token_id)

        if not (str(token_id) == str(pet.user.id) or token_user.is_admin):
            raise NotPetOwnerAccountError()

        queryset = Order.objects.filter(pet=pet)
        return queryset


class OrderListByCustomer(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "customer_id"

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        token_id = self.request.user.id

        customer = get_object_or_404(User, id=customer_id)
        token_user = User.objects.get(id=token_id)

        if not (str(token_id) == str(customer.id) or token_user.is_admin):
            raise CustomerAccountError()

        pets = Pet.objects.filter(user=customer_id)

        queryset = Order.objects.filter(pet=pets[0])

        for pet in pets[1::]:
            queryset = queryset.union(
                Order.objects.filter(pet=pet))

        return queryset


class OrderListByProvider(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "provider_id"

    def get_queryset(self):
        provider_id = self.kwargs['provider_id']
        token_id = self.request.user.id

        user = get_object_or_404(User, id=provider_id)
        token_user = User.objects.get(id=token_id)

        if not user.is_provider:
            raise IdIsNotProvider()
            
        if not (str(token_id) == str(provider_id) or token_user.is_admin):
            raise NotProviderAccountError()

        services = ProviderService.objects.filter(provider=user)

        queryset = Order.objects.filter(service=services[0])

        for service in services[1::]:
            queryset = queryset.union(
                Order.objects.filter(service=service))

        return queryset
