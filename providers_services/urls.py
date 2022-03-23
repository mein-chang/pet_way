from django.urls import path
from .views import ProviderServiceListCreateView, ProviderServiceRetrieveUpdateDestroyView


urlpatterns = [
    path('providers_services/', ProviderServiceListCreateView.as_view()),
    path('providers_services/<str:provider_service_id>/', ProviderServiceRetrieveUpdateDestroyView.as_view())
]
