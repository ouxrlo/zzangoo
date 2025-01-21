from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import ProfileEditForm


def index(request):
    return render(request, "users/index.html")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/signup.html", {"form": form})


@login_required
def profile(request):
    user = request.user
    return render(request, "users/profile.html", {"user": user})


@login_required
def profile_edit(request):
    user = request.user
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = ProfileEditForm(instance=user)

    return render(request, "users/profile_edit.html", {"form": form})
