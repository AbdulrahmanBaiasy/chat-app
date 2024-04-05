from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf import settings
from .forms import LoginForm
from .views import login_auth, register

app_name = "account"


urlpatterns = [
    path("login/", login_auth, name="login"),
    path("register/", register, name="register"),
    path(
        "logout/",
        LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name="logout",
    ),
]
