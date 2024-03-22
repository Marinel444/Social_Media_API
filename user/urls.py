from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import CreateUserView, ManageUserView, UserViewSet, LoginUserView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", CreateUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="me"),
]

app_name = "user"
