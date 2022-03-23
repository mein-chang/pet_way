from django.urls import path
from .views import ProviderInfoListCreateView, ProviderInfoRetrieveUpdateDestroyView

urlpatterns = [
    path('providers_info/', ProviderInfoListCreateView.as_view()),
    path('providers_info/<str:provider_info_id>/', ProviderInfoRetrieveUpdateDestroyView.as_view())
]