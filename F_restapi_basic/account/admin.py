from django.contrib import admin
from .models import UserAccount


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "created_at",
    )
    list_display_links = ("id", "email")
    list_filter = ("last_login", "is_active", "is_staff", "is_superuser")
    raw_id_fields = ("groups", "user_permissions")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("created_at",)
