from rest_framework.exceptions import APIException


class InvalidCodeError(APIException):
    status_code = 401
    default_detail = {'error': 'Invalid code for recovery.'}