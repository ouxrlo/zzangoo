from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.index, name="home"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.user_profile, name="user_profile"),
    path("login/", views.login_view, name="login"),
]
