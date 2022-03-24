from rest_framework.exceptions import APIException


class IdIsNotProvider(APIException):
    status_code = 404
    default_detail = {'error': ['This id does not belong to a provider']}