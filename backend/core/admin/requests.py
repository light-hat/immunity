"""
Отображение в админке унифицированной модели для http-запроса.
"""

from core.models import Request
from django.contrib import admin


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    """
    Отображение http-запроса в админке.
    """

    list_display = (
        "id",
        "application",
        "context",
        "method",
        "path",
        "created_at",
    )
    list_display_links = ("id",)
    list_filter = ("method",)
    search_fields = ("application",)
