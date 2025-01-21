from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.dispatch import receiver


def index(request):
    return render(request, "users/index.html")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users/profile.html")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/signup.html", {"form": form})


User = get_user_model()


@login_required
def user_profile(request):
    user = request.user
    return render(request, "users/profile.html", {"user": user})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("user_page")
        else:
            messages.error(
                request,
                "Please enter a correct username and password. Note that both fields may be case-sensitive.",
            )
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "users/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@receiver(user_logged_out)
def handle_user_logged_out(sender, request, user, **kwargs):
    return redirect("login")
