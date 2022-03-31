from rest_framework.exceptions import APIException


class PetNotExistsError(APIException):
    status_code = 409
    default_detail = {'error': ['Pet does not exists']}


class UserNotFoundError(APIException):
    status_code = 404
    default_detail = {'error': ['User does not exists']}
    
    
    
class PetNotFoundError(APIException):
    status_code = 404
    default_detail = {'error': ['Pet does not exists']}
    
    
class UserDoesNotAddress(APIException):
    status_code = 400
    default_detail = {'error': ['Address not register to this user']}