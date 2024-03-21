from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Post, Comment
from api.serializers import (
    PostSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Comment.objects.filter(author=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer
        if self.action == "retrieve":
            return CommentDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.annotate(likes_count=Count("likes")).all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get("author")
        if author:
            queryset = queryset.filter(author__username__icontains=author)
        return queryset

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({"status": "like removed"}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({"status": "like added"}, status=status.HTTP_200_OK)
