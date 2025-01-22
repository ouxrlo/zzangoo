from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .forms import PostForm
from .serializers import PostSerializer
from .serializers import CommentSerializer
from rest_framework import status
from django.views import View
from django.urls import reverse


class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


# PostDetailView (게시글 상세)
class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"


# PostCreateView (게시글 작성)
class PostCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # 사용자 지정
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )  # 201 상태 코드 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PostUpdateView (게시글 수정)
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def get_success_url(self):
        return reverse_lazy("posts:post_list")


# PostDeleteView (게시글 삭제)
class PostDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 댓글 작성
@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        content = request.POST.get("content")
        Comment.objects.create(post=post, author=request.user, content=content)
    return redirect("posts:post_detail", pk=post.id)


# PostLikeToggleView (게시글 좋아요 토글)
class PostLikeToggleView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect("posts:post_detail", pk=post.id)


class CommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 수정
@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        comment.content = request.POST.get("content")
        comment.save()
    return redirect("posts:post_detail", pk=comment.post.id)


# 댓글 삭제
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    comment.delete()
    return redirect("posts:post_detail", pk=post_id)
