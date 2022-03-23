from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import ProviderService
from .serializers import ProviderServiceSerializer
from rest_framework.authentication import TokenAuthentication
from providers_info.permissions import IsProvider
from users.models import User


class ProviderServiceListCreateView(ListCreateAPIView):
    queryset = ProviderService.objects.all()
    serializer_class = ProviderServiceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProvider]


    def perform_create(self, serializer):
        serializer = serializer.save(provider=self.request.user)
        return serializer


class ProviderServiceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ProviderService.objects.all()
    serializer_class = ProviderServiceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProvider]

    lookup_url_kwarg = 'provider_service_id'
