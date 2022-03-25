from django.urls import path
from .views import OrderListCreateView,OrderRetrieveView, OrderUpdatePutView

urlpatterns = [
    path('orders/',OrderListCreateView.as_view()),
    path('orders/<str:order_id>/',OrderRetrieveView.as_view()),
    path('orders/<str:order_id>/complete/', OrderUpdatePutView.as_view())
]