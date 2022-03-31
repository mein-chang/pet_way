from users.models import User
from users.permissions import OnlyAdminPermission, TokenRecoveryPermission, InvalidCodeError
from users.serializers import UserSerializer, LoginSerializer, GenerateRecoveryCodeSerializer

from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate, TokenAuthentication
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

import os
from dotenv import load_dotenv

load_dotenv()


class UserView(ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [OnlyAdminPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [OnlyAdminPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


class UserLoginView(APIView):

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


class GenerateRecoveryCodeView(APIView):


    def post(self, request):

        serializer = GenerateRecoveryCodeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = request.data['email']

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({'message': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)

        token = Token.objects.get_or_create(user=user)[0]

        email_host_user = str(os.getenv('EMAIL_HOST_USER'))

        subject = 'CÓDIGO PARA RECUPERAÇÃO DE SENHA'
        message = '<h2>Aqui está seu código para recuperação de senha.</h2>' + token.key
        email_from = email_host_user
        recipient_list = [email]

        send_mail(
            subject=subject, message=message, from_email=email_from, recipient_list=recipient_list, fail_silently=False, html_message=message
        )

        return Response({'message': 'Recovery code sent by email.'})


class PasswordRecoveryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [TokenRecoveryPermission]
        # if request.user.is_authenticated == False:
            # raise InvalidCodeError()

    def patch(self, request):

        email = request.user.email
        user = User.objects.filter(email=email).first()

        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            user.set_password(request.data['password'])
            user.save()

            return Response({'message': 'Password updated'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
