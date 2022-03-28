from rest_framework import serializers

from .exceptions import DoesNotHaveAddressError, NotPetOwnerError
from .models import Order
from addresses.models import UserAddress
from addresses.serializers import AddressSerializer
from pets.models import Pet


class OrderSerializer(serializers.ModelSerializer):
    pet_id = serializers.UUIDField(write_only=True)
    service_id = serializers.UUIDField(write_only=True)
    pick_up = AddressSerializer(read_only=True)
    drop = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['created_at', 'completed']
        extra_kwargs = {"rating": {'required': False}}
        depth = 1

    def validate(self, attrs):
        user_id = self.context['request'].user.id
        pick_up_address_id = self.initial_data['pick_up_address_id']
        pet_id = self.initial_data['pet_id']

        if not Pet.objects.filter(user_id=user_id, id=pet_id).exists():
            raise NotPetOwnerError()

        if not UserAddress.objects.filter(user_id=user_id, address_id=pick_up_address_id).exists():
            raise DoesNotHaveAddressError()

        return super().validate(attrs)


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
