from django.urls import path
from .views import ProviderListCreateView


urlpatterns = [
    path('providers/', ProviderListCreateView.as_view())
]