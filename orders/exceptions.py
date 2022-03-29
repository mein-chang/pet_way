from rest_framework.exceptions import APIException


class NotPetOwnerError(APIException):
    status_code = 403
    default_detail = {'error': ['You are not this pet owner.']}


class DoesNotHaveAddressError(APIException):
    status_code = 403
    default_detail = {
        'error': ['You do not have this address register in your account.']}


class DropAddressIsRequiredError(APIException):
    status_code = 400
    default_detail = {
        'error': ['If you are using Pet Taxi service you must pass the drop_address_id.']}


class InvalidUUIDError(APIException):
    status_code = 400
    default_detail = {
        'error': ['You must pass a valid UUID Address.']}


class AddressNotFoundError(APIException):
    status_code = 404
    default_detail = {
        'error': ['Address not found.']}


class NotProviderAccountError(APIException):
    status_code = 403
    default_detail = {
        'error': ['You do not have access to this. Only admin or provider-owner.']}


class NotPetOwnerAccountError(APIException):
    status_code = 403
    default_detail = {
        'error': ['You do not have access to this. Only admin or pet owner.']}


class CustomerAccountError(APIException):
    status_code = 403
    default_detail = {
        'error': ['You do not have access to this. Only admin or customer-owner.']}


class CustomerAccountOnlyError(APIException):
    status_code = 403
    default_detail = {
        'error': ['You do not have access to this. Only pet owner can perform this action.']}


class UpdateError(APIException):
    status_code = 400
    default_detail = {
        'error': ['Please check if you pass the correct id in the field (s).']}
