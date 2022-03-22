from rest_framework import serializers
from .models import Provider
# from users.serializers import UserSerializer


class ProviderSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    class Meta:
        model = Provider
        fields = '__all__'
        