from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import ProviderService
from .serializers import ProviderServiceSerializer
from rest_framework.authentication import TokenAuthentication
from providers_info.permissions import IsProvider
from users.models import User
from django.shortcuts import get_object_or_404


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


class ProviderServiceListByProvider(ListAPIView):
    queryset = ProviderService.objects.all()
    serializer_class = ProviderServiceSerializer

    lookup_url_kwarg = 'provider_id'


    def get_queryset(self):
        provider = get_object_or_404(User, id=self.kwargs['provider_id'])
        queryset = ProviderService.objects.filter(provider=provider)
        return queryset
        