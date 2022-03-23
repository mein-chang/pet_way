from rest_framework.exceptions import APIException


class ProviderInfoAlreadyExistsError(APIException):
    status_code = 409
    default_detail = {'error': ['Provider info already exists']}
