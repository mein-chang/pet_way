from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from providers_info.serializers import ProviderInfoSerializer
from rest_framework.authentication import TokenAuthentication
from .models import ProviderInfo
from providers_info.permissions import IsOwnerProvider, IsProvider
from providers_info.exceptions import ProviderInfoAlreadyExistsError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from drf_yasg import openapi

class ProviderInfoListCreateView(ListCreateAPIView):
    queryset = ProviderInfo.objects.all()
    serializer_class = ProviderInfoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProvider]


    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "instagram": openapi.Schema(type=openapi.TYPE_STRING, description='Instagram'),
        "facebook": openapi.Schema(type=openapi.TYPE_STRING, description='Facebook'),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
        
    }) ,responses={201: ProviderInfoSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'provider_info'):
            raise ProviderInfoAlreadyExistsError()

        serializer = serializer.save(provider=self.request.user)
        return serializer


class ProviderInfoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ProviderInfo.objects.all()
    serializer_class = ProviderInfoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProvider, IsOwnerProvider]

    lookup_url_kwarg = 'provider_info_id'

    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "instagram": openapi.Schema(type=openapi.TYPE_STRING, description='Instagram'),
        "facebook": openapi.Schema(type=openapi.TYPE_STRING, description='Facebook'),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
        
    }) ,responses={200: ProviderInfoSerializer})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "description": openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
        
    }) ,responses={200: ProviderInfoSerializer})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)