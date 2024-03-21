from django.contrib.auth import get_user_model
from django.db.models import OuterRef, Exists
from rest_framework import generics, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user.models import Follow
from user.serializers import UserManagerSerializer, UserListSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserManagerSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserManagerSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        follow_exists = Follow.objects.filter(follower=user, followed=OuterRef("pk"))
        return get_user_model().objects.annotate(is_following=Exists(follow_exists))

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        current_user = request.user
        if current_user == user_to_follow:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow_instance, created = Follow.objects.get_or_create(
            follower=current_user, followed=user_to_follow
        )
        if created:
            return Response(
                {"status": f"You are now following {user_to_follow.username}"},
                status=status.HTTP_201_CREATED,
            )
        else:
            follow_instance.delete()
            return Response(
                {"status": f"You have unfollowed {user_to_follow.username}"},
                status=status.HTTP_204_NO_CONTENT,
            )
