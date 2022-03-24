from django.forms import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .exceptions import AddressNotOwnerError
from .models import Address, UserAddress
from .permissions import IsAdmin
from .serializers import AddressSerializer, AddressCompleteSerializer
from .services import validate_create_address


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


class AddressUpdateView(UpdateAPIView):

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    lookup_url_kwarg = "address_id"

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user_id = self.request.user.id
        address_id = self.kwargs['address_id']

        if UserAddress.objects.filter(user_id=user_id, address_id=address_id).exists():

            number_of_users = UserAddress.objects.filter(
                address_id=address_id).count()

            if number_of_users > 1:
                UserAddress.objects.filter(
                    user_id=user_id, address_id=address_id).delete()

                serializer_request = AddressSerializer(
                    data=serializer.validated_data)

                if serializer_request.is_valid(raise_exception=ValueError):
                    return validate_create_address(user_id, serializer.validated_data)

                return ValidationError(serializer_request.error_messages)

            return super().perform_update(serializer)

        raise AddressNotOwnerError()
