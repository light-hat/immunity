"""
Отображение в админке записей датасета.
"""

from django.contrib import admin

from core.models import DatasetLabel


@admin.register(DatasetLabel)
class DatasetLabelAdmin(admin.ModelAdmin):
    """
    Отображение записей датасета в админке.
    """

    list_display = (
        "id",
        "text",
        "label",
        "created_at",
    )
    list_filter = ("label",)
    list_display_links = ("id",)
