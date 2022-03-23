from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from providers_info.serializers import ProviderInfoSerializer
from rest_framework.authentication import TokenAuthentication
from .models import ProviderInfo
from providers_info.permissions import IsProvider
from users.models import User
from datetime import date


class ProviderInfoListCreateView(ListCreateAPIView):
    queryset = ProviderInfo.objects.all()
    serializer_class = ProviderInfoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsProvider]


    def perform_create(self, serializer):
        # user_test = User.objects.create_user(
        #     email='camila@mail.com',
        #     cpf=12345678901,
        #     birthdate=date.fromisoformat('1994-05-16'),
        #     phone='945838639',
        #     is_provider=True,
        #     is_admin=False
        # )
        serializer = serializer.save(provider=self.request.user)
        # serializer = serializer.save(user=user_test)
        return serializer


class ProviderInfoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ProviderInfo.objects.all()
    serializer_class = ProviderInfoSerializer
    # authorization_classes = [TokenAuthentication]
    # permission_classes = [IsProvider]

    lookup_url_kwarg = 'provider_info_id'
