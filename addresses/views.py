from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication

from .models import Address
from .serializers import AddressSerializer


class AddressListCreateView(ListCreateAPIView):

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    authentication_classes = [TokenAuthentication]
    # permission_classes = []


class AddressRetrieveUpdateView(RetrieveUpdateAPIView):

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    lookup_url_kwarg = "address_id"

    # authentication_classes = [TokenAuthentication]
    # permission_classes = []
