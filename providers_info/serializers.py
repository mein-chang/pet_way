from rest_framework import serializers
from .models import ProviderInfo
from users.models import User


class ProviderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'cpf', 'password', 'birthdate', 'phone', 'date_joined', 'is_provider', 'is_admin', 'provider_info']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1


class ProviderInfoSerializer(serializers.ModelSerializer):
    provider = ProviderUserSerializer(read_only=True)
    class Meta:
        model = ProviderInfo
        fields = '__all__'
        # read_only_fields = ['user']
        # depth = 2
