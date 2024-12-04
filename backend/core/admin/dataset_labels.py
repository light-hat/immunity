"""
Отображение в админке записей датасета.
"""

from core.models import DatasetLabel
from django.contrib import admin


@admin.register(DatasetLabel)
class DatasetLabelAdmin(admin.ModelAdmin):
    """
    Отображение записей датасета в админке.
    """

    list_display = (
        "id",
        "dataset",
        "label",
        "created_at",
    )
    list_display_links = ("id",)
