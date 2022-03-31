from users.models import User
from users.permissions import OnlyAdminPermission
from users.serializers import UserSerializer, LoginSerializer

from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate, TokenAuthentication
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from drf_yasg import openapi

class UserView(ListCreateAPIView):    
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [OnlyAdminPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, description='email@gmail.com'),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description='password'),
        "first_name": openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),
        "cpf": openapi.Schema(type=openapi.TYPE_STRING, description='00000000'),
        "birthdate": openapi.Schema(type=openapi.TYPE_STRING, description='YYYY-MM-DD'),
        "phone": openapi.Schema(type=openapi.TYPE_STRING, description='00-0000000'),
        "is_provider": openapi.Schema(type=openapi.TYPE_BOOLEAN, description='boolean'),
        "is_admin": openapi.Schema(type=openapi.TYPE_BOOLEAN, description='boolean')
        
        
    }) ,responses={201: UserSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserUpdateView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [OnlyAdminPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "first_name": openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),   
    }) ,responses={200: UserSerializer})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, description='email@gmail.com'),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description='password'),
        "first_name": openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),
        "cpf": openapi.Schema(type=openapi.TYPE_STRING, description='00000000'),
        "birthdate": openapi.Schema(type=openapi.TYPE_STRING, description='YYYY-MM-DD'),
        "phone": openapi.Schema(type=openapi.TYPE_STRING, description='00-0000000'),
        "is_provider": openapi.Schema(type=openapi.TYPE_BOOLEAN, description='boolean'),
        "is_admin": openapi.Schema(type=openapi.TYPE_BOOLEAN, description='boolean')
        
        
    }) ,responses={200: UserSerializer})
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class UserLoginView(APIView):
    @swagger_auto_schema(operation_description="description",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, description='email@gmail.com'),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description='string')
    }) ,responses={200: "token"})
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = request.data['email']
        password = request.data['password']

        user = authenticate(email=email, password=password)

        if user:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)