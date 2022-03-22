from rest_framework.generics import ListCreateAPIView
from providers.serializers import ProviderSerializer
from rest_framework.authentication import TokenAuthentication
from .models import Provider
from .permissions import IsProvider

class ProviderListCreateView(ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    # authorization_classes = [TokenAuthentication]
    # permission_classes = [IsProvider]


    def perform_create(self, serializer):
        serializer = serializer.save(user=self.request.user)
        return serializer
