from rest_framework import serializers

from api.models import Post, Comment, Follow


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "description", "image")


class PostListSerializer(PostSerializer):
    author = serializers.StringRelatedField(source="author.username", read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "description",
            "author",
            "likes_count",
            "created_at",
            "updated_at",
            "image",
        )


class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "description",
            "author",
            "created_at",
            "updated_at",
            "image",
            "likes",
        )
