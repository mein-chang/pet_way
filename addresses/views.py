from operator import itemgetter
from django.forms import ValidationError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .exceptions import AddressNotFoundError, AddressNotOwnerError
from .models import Address, UserAddress
from .permissions import IsAdmin
from .serializers import AddressCompleteSerializer, AddressSerializer
from .services import (validate_update_existing_address_or_create,
                       validate_update_existing_address)


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
        return super().update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            user_id = self.request.user.id
            address_id = self.kwargs['address_id']

            serializer_request = AddressSerializer(data=request.data)

            if UserAddress.objects.filter(user_id=user_id, address_id=address_id).exists():

                number_of_users = UserAddress.objects.filter(
                    address_id=address_id).count()

                if number_of_users > 1:
                    validate = validate_update_existing_address_or_create(
                        user_id, address_id, serializer_request)
                    serialized = AddressSerializer(validate)
                    return Response(serialized.data, status=status.HTTP_201_CREATED)

                if not serializer_request.is_valid():
                    validate = validate_update_existing_address(
                        user_id, address_id, serializer_request)
                    serialized = AddressSerializer(validate)
                    return Response(serialized.data, status=status.HTTP_201_CREATED)

            raise AddressNotOwnerError()

        except Address.DoesNotExist:
            raise AddressNotFoundError()

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
