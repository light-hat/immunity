"""
Отображение в админке датасетов.
"""

from django.contrib import admin

from core.models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    """
    Отображение модели датасета в админке.
    """

    list_display = (
        "id",
        "name",
        "type",
        "created_at",
        "updated_at",
    )
    list_display_links = ("name",)
    list_filter = ("type",)
    search_fields = ("name",)
