from rest_framework.exceptions import APIException


class ZipCodeError(APIException):
    status_code = 404
    default_detail = {'error': ['zip_code not found. Please check.']}
