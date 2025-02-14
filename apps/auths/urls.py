from django.urls import path
from rest_framework_simplejwt.views import (
  TokenRefreshView,
)

from apps.auths.views import SignUpView, LoginView, PasswordResetView

app_name = 'api'

urlpatterns = [

  path("login", LoginView.as_view(), name="login"),

  path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),

  path("signup", SignUpView.as_view(), name="signup"),

  path("password-reset", PasswordResetView.as_view(), name="password-reset"),
]