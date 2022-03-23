from rest_framework.urls import path
from users.views import UserView, UserLoginView


urlpatterns = [
    path('users/', UserView.as_view()),
    path('login/', UserLoginView.as_view())
]