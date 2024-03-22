from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User, Follow


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        "email",
        "username",
        "is_staff",
        "is_active",
    ]
    list_filter = ["email", "username", "is_staff", "is_active"]
    fieldsets = (
        (None, {"fields": ("email", "password", "username", "bio", "image")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Follow)
