"""
Отображение конфигурации проектов.
"""

from django.contrib import admin

from core.models import Configuration


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    """
    Отображение конфигурации проекта в админке.
    """

    list_display = (
        "id",
        "project",
        "key",
        "value",
        "vulnerable",
        "created_at",
    )
    list_display_links = ("project",)
    search_fields = ("key",)
