from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Pet
from .serializers import PetSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsClientOrReadOnly, IsOwnerPet
# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from drf_yasg import openapi

class PetCreateListView(ListCreateAPIView):
    
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsClientOrReadOnly]
    
    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description='Name'),
        "birthdate": openapi.Schema(type=openapi.TYPE_STRING, description='YYYY-MM-DD'),
        "specie": openapi.Schema(type=openapi.TYPE_STRING, description='Specie'),
        "breed": openapi.Schema(type=openapi.TYPE_STRING, description='Breed'),
        "gender": openapi.Schema(type=openapi.TYPE_STRING, description='Gender'),
        "size": openapi.Schema(type=openapi.TYPE_STRING, description='Size'),
        
    }) ,responses={201: PetSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
    def get_queryset(self):
        request_user = self.request.user.id
        
        if request_user is not None:
            queryset = Pet.objects.filter(user=request_user)

            return queryset
        
        return super().get_queryset()
    
    
class PetRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsClientOrReadOnly, IsOwnerPet]
    
    
    lookup_url_kwarg = 'pet_id'
    
    
    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description='Name'),
        "birthdate": openapi.Schema(type=openapi.TYPE_STRING, description='YYYY-MM-DD'),
        "specie": openapi.Schema(type=openapi.TYPE_STRING, description='Specie'),
        "breed": openapi.Schema(type=openapi.TYPE_STRING, description='Breed'),
        "gender": openapi.Schema(type=openapi.TYPE_STRING, description='Gender'),
        "size": openapi.Schema(type=openapi.TYPE_STRING, description='Size'),
        
    }) ,responses={200: PetSerializer})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    
    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description='Name')
        
    }) ,responses={200: PetSerializer})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)