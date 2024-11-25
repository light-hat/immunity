"""
Отображение в админке событий потока управления.
"""

from django.contrib import admin

from core.models import Event


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
