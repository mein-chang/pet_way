from django.forms import ValidationError
from operator import itemgetter
import pip._vendor.requests as requests

from .exceptions import AddressConflictError
from .models import Address, UserAddress
from .exceptions import ZipCodeError


def validate_cep(zip_code):
    request = requests.get(f'http://viacep.com.br/ws/{zip_code}/json/')

    if request.status_code == 200:
        data = request.json()

        return data


def validate_cep_request(self, attrs):
    try:
        zip_code = attrs['zip_code']
        via_cep = validate_cep(zip_code)

        attrs['zip_code'] = via_cep['cep']
        attrs['state'] = via_cep['uf']
        attrs['city'] = via_cep['localidade']
        attrs['street'] = via_cep['logradouro']

        return attrs

    except KeyError:
        raise ZipCodeError()

    except TypeError:
        raise ValidationError(
            {'error': ['Invalid zip_code. Only numbers, 8 characters.']})


def validate_exisiting_address(user_id, data):

    zip_code = data['zip_code']
    number = data['number']
    complement = data['complement']
    title = data['title']

    if Address.objects.filter(zip_code=zip_code, number=number, complement=complement).exists():
        address_existent = Address.objects.get(
            zip_code=zip_code, number=number, complement=complement)

        if UserAddress.objects.filter(user_id=user_id, address_id=address_existent.id).exists():
            raise AddressConflictError()

        if address_existent.title == title:
            UserAddress.objects.create(
                user_id=user_id, address_id=address_existent.id)
            return address_existent

    address_new = Address.objects.create(**data)

    UserAddress.objects.create(
        user_id=user_id, address_id=address_new.id)

    return address_new


def validate_update_existing_address_or_create(user_id, address_id, request_data):
    UserAddress.objects.filter(
        user_id=user_id, address_id=address_id).delete()

    current_address = Address.objects.get(id=address_id)

    zip_code_current = current_address.zip_code
    number_current = current_address.number
    complement_current = current_address.complement
    title_current = current_address.title

    if not request_data.is_valid():
        zip_code, number, complement, title = itemgetter(
            'zip_code', 'number', 'complement', 'title')(request_data)

        zip_code = zip_code.value
        number = number.value
        complement = complement.value
        title = title.value

        zip_code_update = zip_code if zip_code is not None else zip_code_current
        number_update = number if number is not None else number_current
        complement_update = complement if complement is not None else complement_current
        title_update = title if title is not None else title_current

        updated = {}
        updated['zip_code'] = zip_code_update
        updated['number'] = number_update
        updated['complement'] = complement_update
        updated['title'] = title_update

        zip_code_filter = zip_code_update[:5] + '-' + zip_code_update[5:]

        if Address.objects.filter(zip_code=zip_code_filter, number=number_update, complement=complement_update).exists():
            address_existent = Address.objects.get(
                zip_code=zip_code_filter, number=number_update, complement=complement_update)

            if UserAddress.objects.filter(user_id=user_id, address_id=address_existent.id).exists():
                raise AddressConflictError()

            if address_existent.title == title_update:
                UserAddress.objects.create(
                    user_id=user_id, address_id=address_existent.id)
                return address_existent

        self = 0
        validate_cep_request(self, updated)
        address_new = Address.objects.create(**updated)

        UserAddress.objects.create(
            user_id=user_id, address_id=address_new.id)

        return address_new


def validate_update_existing_address(user_id, address_id, request_data):

    current_address = Address.objects.get(id=address_id)

    zip_code_current = current_address.zip_code
    number_current = current_address.number
    complement_current = current_address.complement
    title_current = current_address.title

    zip_code, number, complement, title = itemgetter(
        'zip_code', 'number', 'complement', 'title')(request_data)

    zip_code = zip_code.value
    number = number.value
    complement = complement.value
    title = title.value

    zip_code_update = zip_code if zip_code is not None else zip_code_current
    number_update = number if number is not None else number_current
    complement_update = complement if complement is not None else complement_current
    title_update = title if title is not None else title_current

    updated = {}
    updated['zip_code'] = zip_code_update
    updated['number'] = number_update
    updated['complement'] = complement_update
    updated['title'] = title_update

    zip_code_filter = zip_code_update[:5] + '-' + zip_code_update[5:]
    print(zip_code_update)

    if Address.objects.filter(zip_code=zip_code_filter, number=number_update, complement=complement_update).exists():
        address_existent = Address.objects.get(
            zip_code=zip_code_filter, number=number_update, complement=complement_update)
        print(address_existent.title, "add from existent")

        if UserAddress.objects.filter(user_id=user_id, address_id=address_existent.id).exists():
            raise AddressConflictError()

        if address_existent.title == title_update:

            UserAddress.objects.create(
                user_id=user_id, address_id=address_existent.id)
            return address_existent

    self = 0
    validate_cep_request(self, updated)

    Address.objects.filter(id=address_id).update(**updated)

    return Address.objects.get(id=address_id)
