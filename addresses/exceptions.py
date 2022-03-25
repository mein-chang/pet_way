from rest_framework.exceptions import APIException


class ZipCodeError(APIException):
    status_code = 404
    default_detail = {'error': ['zip_code not found. Please check.']}


class AddressConflictError(APIException):
    status_code = 409
    default_detail = {
        'error': ['This address is already registered for this user.']}


class AddressNotOwnerError(APIException):
    status_code = 403
    default_detail = {
        'error': ['You do not have permission to perform this action. You must have this address registered in your account.']}


class AddressNotFoundError(APIException):
    status_code = 404
    default_detail = {
        'error': ['Address not found. Please check.']}
