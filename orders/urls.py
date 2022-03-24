from django.urls import path
from .views import OrderListCreateView,OrderRetrieveView

urlpatterns = [
    path('orders/',OrderListCreateView.as_view()),
    path('orders/<str:order_id>',OrderRetrieveView.as_view())
]