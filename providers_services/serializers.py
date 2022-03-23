from rest_framework import serializers
from providers_info.serializers import ProviderUserSerializer
from .models import ProviderService


class ProviderServiceSerializer(serializers.ModelSerializer):
    provider = ProviderUserSerializer(read_only=True)
    class Meta:
        model = ProviderService
        fields = '__all__'
        # depth = 2
