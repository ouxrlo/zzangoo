from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts:post_list")  # 회원가입 후 게시글 목록으로 이동
    else:
        form = UserCreationForm()
    return render(request, "users/signup.html", {"form": form})
