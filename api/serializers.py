from rest_framework import serializers

from api.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "text", "author", "post", "updated_at", "created_at")


class CommentListSerializer(CommentSerializer):
    post = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "post", "text")

    def get_post(self, obj):
        return str(obj.post)


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
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

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
            "is_liked",
            "comments",
        )

    def get_is_liked(self, obj):
        user = self.context["request"].user
        return obj.likes.filter(id=user.id).exists()


class CommentDetailSerializer(CommentSerializer):
    post = PostListSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "post", "text", "updated_at", "created_at")
