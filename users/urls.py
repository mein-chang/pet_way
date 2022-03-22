from rest_framework.urls import path
from users.views import ListCreateAPIView, UserLoginView


urlpatterns = [
    path('users/', ListCreateAPIView.as_view()),
    path('login/', UserLoginView.as_view())
]