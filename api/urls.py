from django.urls import path, include
from rest_framework import routers

from api.views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"comments", CommentViewSet, basename="comments")


urlpatterns = [path("", include(router.urls))]

app_name = "api"
