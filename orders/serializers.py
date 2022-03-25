from .models import Order
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    pet_id = serializers.UUIDField(write_only=True)
    service_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Order
        fields = "__all__"
        extra_kargs = {"id":{'read_only':True},"created_at":{'read_only':True},"rating":{'required':False}}
        depth = 1