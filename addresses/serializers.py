from rest_framework import serializers

from .models import Address
from .services import validate_exisiting_address, validate_cep_request
from users.serializers import UserSerializer


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'zip_code', 'state', 'city',
                  'street', 'number', 'complement', 'title']
        extra_kwargs = {'state': {'read_only': True}, 'city': {
            'read_only': True}, 'street': {'read_only': True}}

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            valid = validate_cep_request(self, attrs)
            return super().validate(valid)

        if self.context['request'].method == 'PATCH':
            try:
                if self.initial_data['zip_code']:
                    valid = validate_cep_request(self, attrs)
                    return super().validate(valid)

            except KeyError:
                return super().validate(attrs)

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        return validate_exisiting_address(user_id, validated_data)


class AddressCompleteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Address
        fields = '__all__'
