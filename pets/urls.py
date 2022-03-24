from django.urls import path
from .views import PetCreateListView, PetRetrieveUpdateDestroyView

urlpatterns = [
    path('pets/', PetCreateListView.as_view()),
    path('pets/<str:pet_id>/', PetRetrieveUpdateDestroyView.as_view())
]