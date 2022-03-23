import pip._vendor.requests as requests

from .exceptions import AddressConflictError
from .models import Address, UserAddress


def validate_cep(zip_code):
    request = requests.get(f'http://viacep.com.br/ws/{zip_code}/json/')

    if request.status_code == 200:
        data = request.json()

        return data


def validate_create_address(user_id, data):
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
