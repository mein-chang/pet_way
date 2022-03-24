from django.urls import path
from .views import ProviderServiceListCreateView, ProviderServiceRetrieveUpdateDestroyView, ProviderServiceListByProvider


urlpatterns = [
    path('providers_services/', ProviderServiceListCreateView.as_view()),
    path('providers_services/<str:provider_service_id>/', ProviderServiceRetrieveUpdateDestroyView.as_view()),
    path('providers_services/provider/<str:provider_id>/', ProviderServiceListByProvider.as_view())
]
