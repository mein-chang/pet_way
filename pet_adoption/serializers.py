from datetime import datetime
from rest_framework import serializers

from pet_adoption.exceptions import PetNotExistsError
from .models import PetAdoption
from users.models import User
from pets.models import Pet
from users.serializers import UserSerializer
from pets.serializers import PetSerializer

class PetAdoptionSerializer(serializers.ModelSerializer):
    castrated = serializers.BooleanField()
    is_vaccinated = serializers.BooleanField()
    additional_info = serializers.CharField()
    is_health = serializers.BooleanField()
    available = serializers.BooleanField()
    pet_id = serializers.UUIDField(write_only=True)
    adopter = UserSerializer(read_only=True)
    pet = PetSerializer(read_only=True)
    
    class Meta: 
        model = PetAdoption
        fields = ['id', 'castrated', 'is_vaccinated', 'is_health', 'additional_info','available', 'pet_id', 'pet', 'adopted_at', 'adopter']        
    
        
    def create(self, validated_data):
        
        pet_id = validated_data['pet_id']
        
        pet = Pet.objects.filter(id=pet_id).first()
        
        
        if pet == None:
            raise PetNotExistsError()
    
        adoption_pet = PetAdoption.objects.create(**validated_data,user=self.context['request'].user ,pet=pet)
        
        return adoption_pet
    
    