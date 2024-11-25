"""
Отображение в админке унифицированной модели для запроса и ответа.
"""

from django.contrib import admin

from core.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Отображение унифицированной модели для запроса и ответа в админке.
    """

    list_display = (
        "id",
        "application",
        "context",
        "type",
        "method",
        "path",
        "status_code",
        "created_at",
    )
    list_display_links = ("id",)
    list_filter = ("type", "method", "status_code")
    search_fields = ("application",)
