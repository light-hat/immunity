"""
Отображение модели пользовтаеля системы.
"""

from django.contrib import admin

from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Отображение пользователя в админке.
    """

    list_display = (
        "username",
        "email",
        "role",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_display_links = ("username",)
    list_filter = ("username", "email", "first_name", "last_name")
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
    list_editable = ("is_staff", "is_active")
