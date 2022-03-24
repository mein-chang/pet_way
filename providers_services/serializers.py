from rest_framework import serializers

from providers_info.serializers import BasicProviderInfoSerializer
from .models import ProviderService
from users.models import User


class ProviderUserSerializer(serializers.ModelSerializer):
    provider_info = BasicProviderInfoSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'cpf', 'birthdate', 
        'phone', 'is_provider', 'is_admin', 'date_joined', 'provider_info']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}


class ProviderServiceSerializer(serializers.ModelSerializer):
    provider = ProviderUserSerializer(read_only=True)
    class Meta:
        model = ProviderService
        fields = '__all__'


class BasicProviderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderService
        fields = '__all__'
