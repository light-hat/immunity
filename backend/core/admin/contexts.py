"""
Отображение модели контекста выполнения запроса.
"""

from core.models import Context
from django.contrib import admin


@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    """
    Отображение контекста выполнения запроса в админке.
    """

    list_display = (
        "id",
        "application",
        "created_at",
    )
    list_display_links = ("id",)
    search_fields = ("application",)
