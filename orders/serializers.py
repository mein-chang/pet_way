from .models import Order
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    pet_id = serializers.UUIDField(write_only=True)
    service_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['created_at', 'completed']
        extra_kwargs = {"rating":{'required':False}}
        depth = 1


class OrderUpdatePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['service_date', 'created_at']
        extra_kwargs = {"completed": {"required": True}}


class OrderUpdatePatchSerializer(serializers.ModelSerializer):
    pet_id = serializers.UUIDField(write_only=True)
    service_id = serializers.UUIDField(write_only=True)
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['completed', 'created_at', 'rating']