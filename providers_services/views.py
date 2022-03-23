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
        # provider = User.objects.get(id="d9f800db89b0425fa1f59b77af756ab1")
        # import ipdb
        # ipdb.set_trace()
        # serializer = serializer.save(provider=provider.provider)
        serializer = serializer.save(provider=self.request.user)
        return serializer


class ProviderServiceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ProviderService.objects.all()
    serializer_class = ProviderServiceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProvider]

    lookup_url_kwarg = 'provider_service_id'
