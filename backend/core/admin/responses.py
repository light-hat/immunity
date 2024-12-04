"""
Отображение в админке унифицированной модели для http-ответа.
"""

from core.models import Response
from django.contrib import admin


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    """
    Отображение http-ответа в админке.
    """

    list_display = (
        "id",
        "application",
        "context",
        "content_type",
        "content_length",
        "charset",
        "status_code",
        "created_at",
    )
    list_display_links = ("id",)
    list_filter = ("status_code",)
    search_fields = ("application",)
