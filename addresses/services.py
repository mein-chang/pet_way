from django.forms import ValidationError
import pip._vendor.requests as requests


def validate_cep(zip_code):
    request = requests.get(f'http://viacep.com.br/ws/{zip_code}/json/')

    if request.status_code == 200:
        data = request.json()

        return data
