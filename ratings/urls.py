from django.urls import path
from .views import RaitingListCreateView


urlpatterns = [
    path('ratings/', RaitingListCreateView.as_view())
]
