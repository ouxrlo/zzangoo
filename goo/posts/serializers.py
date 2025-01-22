from rest_framework import serializers
from users.serializers import (
    UserSerializer,
)
from .models import Post
from .models import Comment


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at", "updated_at"]
