"""
Отображение в админке унифицированной модели для http-запроса.
"""

from django.contrib import admin

from core.models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    """
    Отображение http-запроса в админке.
    """

    list_display = (
        "id",
        "project",
        "context",
        "method",
        "path",
        "created_at",
    )
    list_display_links = ("id",)
    list_filter = ("method",)
    search_fields = ("project",)
