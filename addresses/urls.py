from django.urls import path
from .views import AddressCreateListView, AddressListView, AddressUpdateView


urlpatterns = [
    path('users/addresses/', AddressListView.as_view()),
    path('addresses/', AddressCreateListView.as_view()),
    path('addresses/<str:address_id>/', AddressUpdateView.as_view())
]
