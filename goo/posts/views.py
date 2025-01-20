from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .forms import PostForm
from .models import Post, get_user_model


def post_list(request):
    post = Post.objects.all()
    paginator = Paginator(post, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "posts/post_list.html", {"page_obj": page_obj})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "posts/post_detail.html", {"post": post})


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


from django.shortcuts import get_object_or_404, redirect
from .models import Post
from .forms import PostForm


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:post_list")
    else:
        form = PostForm(instance=post)

    return render(request, "posts/post_form.html", {"form": form})
