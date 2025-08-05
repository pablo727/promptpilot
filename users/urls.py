from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, custom_logout, SignUpView

app_name = "users"
urlpatterns = [
    path("home/", home, name="home"),
    path("logout/", custom_logout, name="logout"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("signup/", SignUpView.as_view(), name="signup"),
]
