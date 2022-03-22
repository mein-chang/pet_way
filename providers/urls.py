from django.urls import path
from .views import ProviderListCreateView, ProviderRetrieveUpdateDestroyView

urlpatterns = [
    path('providers/', ProviderListCreateView.as_view()),
    path('providers/<str:provider_id>/', ProviderRetrieveUpdateDestroyView.as_view())
]