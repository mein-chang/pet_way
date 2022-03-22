from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from providers.serializers import ProviderSerializer
from rest_framework.authentication import TokenAuthentication
from .models import Provider
from .permissions import IsProvider
from users.models import User
from datetime import date

class ProviderListCreateView(ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    # authorization_classes = [TokenAuthentication]
    # permission_classes = [IsProvider]


    def perform_create(self, serializer):
        user_test = User.objects.create_user(
            email='camila@mail.com',
            cpf=12345678901,
            birthdate=date.fromisoformat('1994-05-16'),
            phone='945838639',
            is_provider=True,
            is_admin=False
        )
        # serializer = serializer.save(user=self.request.user)
        serializer = serializer.save(user=user_test)
        return serializer


class ProviderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    # authorization_classes = [TokenAuthentication]
    # permission_classes = [IsProvider]

    lookup_url_kwarg = 'provider_id'
