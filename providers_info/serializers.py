from rest_framework import serializers
from users.serializers import UserSerializer
from .models import ProviderInfo


class ProviderInfoSerializer(serializers.ModelSerializer):
    provider = UserSerializer(read_only=True)
    class Meta:
        model = ProviderInfo
        fields = '__all__'


class BasicProviderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderInfo
        exclude = ['id', 'provider']