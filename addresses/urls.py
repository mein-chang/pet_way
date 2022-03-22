from django.urls import path
from .views import AddressListCreateView, AddressRetrieveUpdateView


urlpatterns = [
    path('addresses/', AddressListCreateView.as_view()),
    path('addresses/<str:address_id>/', AddressRetrieveUpdateView.as_view())
]
