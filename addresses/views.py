from traceback import print_tb
from django.forms import ValidationError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .exceptions import AddressNotOwnerError, AddressNotFoundError
from .models import Address, UserAddress
from .permissions import IsAdmin
from .serializers import AddressCompleteSerializer, AddressSerializer
from .services import validate_create_address
from users.models import User
from operator import itemgetter


class AddressCreateListView(ListCreateAPIView):

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.id
        return Address.objects.filter(users=user)


class AddressListView(ListAPIView):

    queryset = Address.objects.all()
    serializer_class = AddressCompleteSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]


class AddressUpdateView(RetrieveUpdateDestroyAPIView):

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    lookup_url_kwarg = "address_id"

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user_id = self.request.user.id
        address_id = self.kwargs['address_id']

        if UserAddress.objects.filter(user_id=user_id, address_id=address_id).exists():

            number_of_users = UserAddress.objects.filter(
                address_id=address_id).count()

            if number_of_users > 1:
                UserAddress.objects.filter(
                    user_id=user_id, address_id=address_id).delete()

                serializer_request = AddressSerializer(
                    data=request.data)

                if serializer_request.is_valid(raise_exception=ValueError):
                    validate = validate_create_address(
                        user_id, serializer_request.validated_data)
                    serialized = AddressSerializer(validate)
                    return Response(serialized.data, status=status.HTTP_201_CREATED)

                return ValidationError(serializer_request.error_messages)

            return super().update(request, *args, **kwargs)

        raise AddressNotOwnerError()

    def delete(self, request, *args, **kwargs):
        try:
            user_id = self.request.user.id
            address_id = self.kwargs['address_id']

            Address.objects.get(id=address_id)

            number_of_users = UserAddress.objects.filter(
                address_id=address_id).count()

            if UserAddress.objects.filter(user_id=user_id, address_id=address_id).exists():

                if number_of_users > 1:
                    UserAddress.objects.filter(
                        user_id=user_id, address_id=address_id).delete()
                    return Response({}, status=status.HTTP_204_NO_CONTENT)

                return super().delete(request, *args, **kwargs)

            raise AddressNotOwnerError()

        except Address.DoesNotExist:
            raise AddressNotFoundError()


class AddressListProvidersView(ListAPIView):

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        providers_address = Address.objects.filter(users__is_provider=True)

        state = self.request.GET.get('state', None)
        city = self.request.GET.get('city', None)

        if state and city is not None:
            providers_address = providers_address.filter(
                state=state.upper(), city=city.capitalize())

        if state is not None:
            providers_address = providers_address.filter(state=state.upper())

        if city is not None:
            providers_address = providers_address.filter(
                city=city.capitalize())

        return providers_address
