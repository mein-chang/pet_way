from django.forms import ValidationError
from rest_framework import serializers

from .exceptions import ZipCodeError
from .models import Address
from .services import validate_cep, validate_create_address
from users.serializers import UserSerializer


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'zip_code', 'state', 'city',
                  'street', 'number', 'complement', 'title']
        extra_kwargs = {'state': {'read_only': True}, 'city': {
            'read_only': True}, 'street': {'read_only': True}}

    def validate(self, attrs):
        try:
            zip_code = attrs['zip_code']
            via_cep = validate_cep(zip_code)

            attrs['zip_code'] = via_cep['cep']
            attrs['state'] = via_cep['uf']
            attrs['city'] = via_cep['localidade']
            attrs['street'] = via_cep['logradouro']

            return super().validate(attrs)

        except KeyError:
            raise ZipCodeError()

        except TypeError:
            raise ValidationError(
                {'error': ['Invalid zip_code. Only numbers, 8 characters.']})

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        return validate_create_address(user_id, validated_data)


class AddressCompleteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Address
        fields = '__all__'
