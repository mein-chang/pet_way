from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'cpf', 'birthdate', 
        'phone', 'is_provider', 'is_admin', 'date_joined', ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()