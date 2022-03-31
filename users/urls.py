from rest_framework.urls import path
from users.views import UserView, UserLoginView, UserUpdateView, GenerateRecoveryCodeView, PasswordRecoveryView


urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/<str:id>/', UserUpdateView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('recovery-password-code/', GenerateRecoveryCodeView.as_view()),
    path('recovery-password/', PasswordRecoveryView.as_view())
]