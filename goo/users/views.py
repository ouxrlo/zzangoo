from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model


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
