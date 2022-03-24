from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import ProviderService
from .serializers import BasicProviderServiceSerializer, ProviderServiceSerializer
from rest_framework.authentication import TokenAuthentication
from providers_info.permissions import IsProvider
from users.models import User
from django.shortcuts import get_object_or_404
from .exceptions import IdIsNotProvider


class ProviderServiceListCreateView(ListCreateAPIView):
    queryset = ProviderService.objects.all()
    serializer_class = ProviderServiceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProvider]


    def perform_create(self, serializer):
        serializer = serializer.save(provider=self.request.user)
        return serializer


    def filter_queryset(self, queryset):
        if 'type' in self.request.query_params:
            service_type = self.request.GET.get('type').replace(self.request.GET.get('type')[3:4], ' ')
            queryset = queryset.filter(type__icontains=service_type)

        return super().filter_queryset(queryset)


class ProviderServiceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ProviderService.objects.all()
    serializer_class = ProviderServiceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProvider]

    lookup_url_kwarg = 'provider_service_id'


class ProviderServiceListByProvider(ListAPIView):
    queryset = ProviderService.objects.all()
    serializer_class = BasicProviderServiceSerializer

    lookup_url_kwarg = 'provider_id'


    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['provider_id'])
        
        if not user.is_provider:
            raise IdIsNotProvider() 

        queryset = ProviderService.objects.filter(provider=user)
        return queryset
        