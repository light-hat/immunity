"""
Отображение модели приложения.
"""

from django.contrib import admin

from core.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Отображение приложения в админке.
    """

    list_display = (
        "id",
        "name",
        "language",
        "created_at",
        "last_online",
    )
    list_display_links = ("name",)
    list_filter = ("language",)
    search_fields = (
        "id",
        "name",
        "language",
        "created_at",
        "last_online",
    )
