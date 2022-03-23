from users.models import User
from users.permissions import OnlyAdminPermission
from users.serializers import UserSerializer, LoginSerializer

from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate, TokenAuthentication
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserView(ListCreateAPIView, UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [OnlyAdminPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer


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