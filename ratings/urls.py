from django.urls import path
from .views import RatingPetView,RatingProviderView

urlpatterns = [
    path('orders/<str:order_id>/rating/pet/',RatingPetView.as_view()),
    path('orders/<str:order_id>/rating/provider/',RatingProviderView.as_view()),
    
]