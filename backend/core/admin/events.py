"""
Отображение в админке событий потока управления.
"""

from core.models import Event
from django.contrib import admin


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Отображение событий потока управления в админке.
    """

    list_display = (
        "id",
        "context",
        "application",
        "timestamp",
        "type",
        "func_name",
        "module",
        "filename",
    )
    list_display_links = ("id",)
    list_filter = ("type",)
    search_fields = ("application",)
