from datetime import datetime
from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from addresses.models import UserAddress
from pet_adoption.exceptions import PetNotExistsError, PetNotFoundError, UserDoesNotAddress, UserNotFoundError
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .models import PetAdoption
from .serializers import PetAdoptionSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
# Create your views here.


class PetAdoptionCreateListView(ListCreateAPIView):
    
    queryset = PetAdoption.objects.all()
    serializer_class = PetAdoptionSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def filter_queryset(self, queryset):
        queryset = queryset.filter(available=True)
        return super().filter_queryset(queryset)


class PetUpdateView(UpdateAPIView):
    queryset = PetAdoption.objects.all()
    serializer_class = PetAdoptionSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    lookup_url_kwarg = 'adoption_id'
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):

        adopter_id = request.data['adopter_id']
        pet_id = self.kwargs['adoption_id']
        
        try:
            user_found = User.objects.get(id=adopter_id)
            
        except:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
        pet_found = get_object_or_404(PetAdoption, id=pet_id)

        if UserAddress.objects.filter(user=adopter_id).count() < 1:
            raise UserDoesNotAddress()
        
        pet_found.adopter = user_found
        pet_found.available = False
        pet_found.adopted_at = datetime.now()    
        
        pet_found.save()
        
        serialized = PetAdoptionSerializer(pet_found)
        
        return Response(serialized.data, status=status.HTTP_200_OK)
    