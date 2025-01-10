"""
Отображение зависимостей проектов.
"""

from django.contrib import admin

from core.models import Library


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    """
    Отображение зависимости проекта в админке.
    """

    list_display = (
        "id",
        "project",
        "key",
        "value",
        "vulnerable",
        "created_at",
    )
    list_display_links = ("project",)
    search_fields = ("key",)
