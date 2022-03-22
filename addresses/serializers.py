from django.forms import ValidationError
from rest_framework import serializers

from petway.exceptions import ZipCodeError

from .models import Address, UserAddress
from .services import validate_cep
# from users.serializers import UserSerializer


class AddressSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Address
        fields = '__all__'
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
        zip_code = validated_data['zip_code']
        number = validated_data['number']
        complement = validated_data['complement']

        if Address.objects.filter(zip_code=zip_code, number=number, complement=complement).exists():
            address_existent = Address.objects.get(
                zip_code=zip_code, number=number, complement=complement)

            UserAddress.objects.create(
                user_id=self.context['request'].user.id, address_id=address_existent.id)
            return address_existent

        new_address = Address.objects.create(**validated_data)
        UserAddress.objects.create(
            user_id=self.context['request'].user.id, address_id=new_address.id)

        return new_address
