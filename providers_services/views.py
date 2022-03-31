from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import ProviderService
from .serializers import BasicProviderServiceSerializer, ProviderServiceSerializer
from rest_framework.authentication import TokenAuthentication
from providers_info.permissions import IsOwnerProvider, IsProvider
from users.models import User
from django.shortcuts import get_object_or_404
from .exceptions import IdIsNotProvider

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from drf_yasg import openapi

class ProviderServiceListCreateView(ListCreateAPIView):
    queryset = ProviderService.objects.all()
    serializer_class = ProviderServiceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProvider]


    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "type": openapi.Schema(type=openapi.TYPE_STRING, description='type'),
        "price": openapi.Schema(type=openapi.TYPE_NUMBER, description='price'),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
        
    }) ,responses={201: ProviderServiceSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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
    permission_classes = [IsProvider, IsOwnerProvider]

    lookup_url_kwarg = 'provider_service_id'


class ProviderServiceListByProvider(ListAPIView):
    queryset = ProviderService.objects.all()
    serializer_class = BasicProviderServiceSerializer

    lookup_url_kwarg = 'provider_id'


    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "type": openapi.Schema(type=openapi.TYPE_STRING, description='type'),
        "price": openapi.Schema(type=openapi.TYPE_NUMBER, description='price'),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
        
    }) ,responses={200: ProviderServiceSerializer})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "description": openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
        
    }) ,responses={200: ProviderServiceSerializer})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['provider_id'])
        
        if not user.is_provider:
            raise IdIsNotProvider() 

        queryset = ProviderService.objects.filter(provider=user)
        return queryset
        