from .models import Order
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        extra_kargs = {"id":{'read_only':True},"created_at":{'read_only':True},"rating":{'required':False}}
        depth = 1