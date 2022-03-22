from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Service
from .serializers import ServiceSerializer
from rest_framework.authentication import TokenAuthentication

from users.models import User


class ServiceListCreateView(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    # authorization_classes = [TokenAuthentication]
    # permission_classes = []


    def perform_create(self, serializer):
        provider = User.objects.get(id="d9f800db89b0425fa1f59b77af756ab1")

        serializer = serializer.save(provider=provider.provider)
        # serializer = serializer.save(provider=self.request.user.provider)
        return serializer


class ServiceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    # authorization_classes = [TokenAuthentication]
    # permission_classes = []

    lookup_url_kwarg = 'service_id'
