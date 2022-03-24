from django.forms import ValidationError
from rest_framework import serializers

from pets.exceptions import PetAlreadyExistsError
from users.serializers import UserSerializer
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    birthdate = serializers.DateField()
    specie = serializers.CharField()
    breed = serializers.CharField()
    gender = serializers.CharField()
    size = serializers.CharField()
    user = UserSerializer(read_only=True)


    class Meta:
        model = Pet
        fields = '__all__'


    def create(self, validated_data):
        name = validated_data['name']
        if self.context['request'].user.is_provider == False and self.context['request'].user.is_admin == False:
            petName = Pet.objects.filter(name=name).first()
            
            if petName:
                raise PetAlreadyExistsError()
            
            
            return Pet.objects.create(**validated_data, user=self.context['request'].user)


