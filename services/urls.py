from django.urls import path
from .views import ServiceListCreateView, ServiceRetrieveUpdateDestroyView


urlpatterns = [
    path('services/', ServiceListCreateView.as_view()),
    path('services/<str:service_id>/', ServiceRetrieveUpdateDestroyView.as_view())
]
