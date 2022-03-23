from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Pet
from .serializers import PetSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsClientOrReadOnly, IsOwnerPet
# Create your views here.

class PetCreateListView(ListCreateAPIView):
    
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsClientOrReadOnly]
    
    
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
