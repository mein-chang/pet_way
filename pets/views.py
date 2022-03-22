# from django.shortcuts import render
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from .models import Pet
# from .serializers import PetSerializer
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from permissions import IsClientOrReadOnly, IsOwnerPet
# # Create your views here.

# class PetCreateListView(ListCreateAPIView):
    
#     queryset = Pet.objects.all()
#     serializer_class = PetSerializer

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated,IsClientOrReadOnly]
    
    
# class PetRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    
#     queryset = Pet.objects.all()
#     serializer_class = PetSerializer

#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsClientOrReadOnly, IsOwnerPet]
    
    
#     lookup_url_kwarg = 'pet_id'