from django.urls import path
from .views import PetAdoptionCreateListView, PetUpdateView
urlpatterns = [
    path('adoption/', PetAdoptionCreateListView.as_view()),
    path('adoption/<str:adoption_id>/', PetUpdateView.as_view())
]