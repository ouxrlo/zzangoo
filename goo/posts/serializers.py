from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at", "updated_at"]
        read_only_fields = ["post", "author", "created_at", "updated_at"]

    def create(self, validated_data):
        post = self.context["post"]
        author = self.context["author"]
        return Comment.objects.create(post=post, author=author, **validated_data)
