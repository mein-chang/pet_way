from .models import Order
from rest_framework import generics
from .serializers import OrderSerializer
from providers_services.models import ProviderService

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    def perform_create(self, serializer):
        service = ProviderService.objects.get(id=self.request.data['service_id'])
        serializer = serializer.save(service=service)
        return super().perform_create(serializer)


class OrderRetrieveView(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = "order_id"