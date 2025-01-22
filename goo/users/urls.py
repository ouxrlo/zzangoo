from django.urls import path
from .views import IndexView, SignupView, LoginView, UserProfileView, ProfileEditView

app_name = "users"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
]
