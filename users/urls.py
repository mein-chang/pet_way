from rest_framework.urls import path
from users.views import UserView, UserLoginView, UserUpdateView


urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/<str:id>', UserUpdateView.as_view()),
    path('login/', UserLoginView.as_view())
]