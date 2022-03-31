from django.urls import path
from .views import OrderListCreateView, OrderRetrieveView, OrderUpdatePutView, OrderListByPet, OrderListByCustomer, OrderListByProvider

urlpatterns = [
    path('orders/', OrderListCreateView.as_view()),
    path('orders/<str:order_id>/', OrderRetrieveView.as_view()),
    path('orders/<str:order_id>/complete/', OrderUpdatePutView.as_view()),
    path('orders/pet/<str:pet_id>/', OrderListByPet.as_view()),
    path('orders/customer/<str:customer_id>/', OrderListByCustomer.as_view()),
    path('orders/provider/<str:provider_id>/', OrderListByProvider.as_view())
]
