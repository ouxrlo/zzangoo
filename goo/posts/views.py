from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Comment, Post, get_user_model
from .serializers import CommentSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# 댓글 작성 시 인증되지 않은 사용자가 접근하는 경우를 방지 DRF의 권한 체크
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


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
def post_like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
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
def post_like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
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


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def comment_list(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "GET":
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        content = request.POST.get("content")
        Comment.objects.create(post=post, author=request.user, content=content)
    return redirect("posts:post_detail", pk=post.id)


@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        comment.content = request.POST.get("content")
        comment.save()
    return redirect("posts:post_detail", pk=comment.post.id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    comment.delete()
    return redirect("posts:post_detail", pk=post_id)
