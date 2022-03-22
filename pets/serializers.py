# from rest_framework import serializers

# from pets.exceptions import PetAlreadyExistsError
# from .models import Pet

# class PetSerializer(serializers.ModelSerializer):
#     name = serializers.CharField()
#     birthdate = serializers.DateField()
#     specie = serializers.CharField()
#     breed = serializers.CharField()
#     gender = serializers.CharField()
#     size = serializers.CharField()
#  #  user = UserSeriaizer(read_only=True) 
 
 
#     class Meta:
#         model = Pet
#         fields = '__all__'
        
    
#     def validate(self, attrs):
#         name = attrs['name']
        
#         petName = Pet.objects.filter(name=name).first()
        
#         if petName:
#             raise PetAlreadyExistsError() 
        
#         return super().validate(attrs)
        
#     def create(self, validated_data):
#         return Pet.objects.create(**validated_data, user=self.context['request'].user)