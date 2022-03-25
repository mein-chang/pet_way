from rest_framework import generics
from .serializers import OrderSerializer, OrderUpdatePutSerializer, OrderUpdatePatchSerializer
from pets.models import Pet
from providers_services.models import ProviderService
from django.shortcuts import get_object_or_404
from providers_services.exceptions import IdIsNotProvider
from users.models import User
from .models import Order

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    def perform_create(self, serializer):
        pet = Pet.objects.get(id=self.request.data["pet_id"])
        service = ProviderService.objects.get(id=self.request.data["service_id"])
        serializer = serializer.save(pet=pet, service=service)
        return super().perform_create(serializer)


class OrderRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = "order_id"


    def get_serializer_class(self):

        if self.request.method == "PATCH":
            return OrderUpdatePatchSerializer 

        return super().get_serializer_class()


    def perform_update(self, serializer):
       
        if "pet_id" in self.request.data and "service_id" in self.request.data:
            pet = get_object_or_404(Pet, id=self.request.data["pet_id"])
            service = get_object_or_404(ProviderService, id=self.request.data["service_id"])
            serializer = serializer.save(pet=pet, service=service)
        
        elif "pet_id" in self.request.data:
            pet = get_object_or_404(Pet, id=self.request.data["pet_id"])
            serializer = serializer.save(pet=pet)
    
        elif "service_id" in self.request.data:
            service = get_object_or_404(ProviderService, id=self.request.data["service_id"])
            serializer = serializer.save(service=service)

        return super().perform_update(serializer)


class OrderUpdatePutView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdatePutSerializer
    lookup_url_kwarg = "order_id"


class OrderListByPet(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = "pet_id"


    def get_queryset(self):
        pet = get_object_or_404(Pet, id=self.kwargs['pet_id'])

        queryset = Order.objects.filter(pet=pet)
        return queryset


class OrderListByProvider(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = "provider_id"


    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['provider_id'])
        
        if not user.is_provider:
            raise IdIsNotProvider()

        services = ProviderService.objects.filter(provider=user)
        
        queryset = Order.objects.filter(service=services[0])
   
        for service in services[1::]:
            queryset = queryset.union(Order.objects.filter(service=service))
        
        return queryset