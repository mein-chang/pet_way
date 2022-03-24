from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from providers_info.serializers import ProviderInfoSerializer
from rest_framework.authentication import TokenAuthentication
from .models import ProviderInfo
from providers_info.permissions import IsProvider
from users.models import User
from datetime import date


class ProviderInfoListCreateView(ListCreateAPIView):
    queryset = ProviderInfo.objects.all()
    serializer_class = ProviderInfoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProvider]


    def perform_create(self, serializer):
        serializer = serializer.save(provider=self.request.user)
        return serializer


class ProviderInfoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ProviderInfo.objects.all()
    serializer_class = ProviderInfoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProvider]

    lookup_url_kwarg = 'provider_info_id'