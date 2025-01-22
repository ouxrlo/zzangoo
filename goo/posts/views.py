from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .forms import PostForm
from .models import Post, get_user_model
from django.contrib.auth.decorators import login_required


@login_required
def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "posts/post_list.html", {"page_obj": page_obj})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "posts/post_detail.html", {"post": post})


@login_required
def post_like_toggle(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect("posts:post_detail", pk=post.id)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = get_user_model().objects.get(id=request.user.id)
            post.save()
            return redirect("posts:post_list")
    else:
        form = PostForm()
    return render(request, "posts/post_form.html", {"form": form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return redirect("posts:post_list")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:post_list")
    else:
        form = PostForm(instance=post)
    return render(request, "posts/post_form.html", {"form": form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("posts:post_list")
    return render(request, "posts/post_confirm_delete.html", {"post": post})
