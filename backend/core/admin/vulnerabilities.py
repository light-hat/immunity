"""
Отображение в админке найденных уязвимостей.
"""

from django.contrib import admin

from core.models import Vulnerability


@admin.register(Vulnerability)
class VulnerabilityAdmin(admin.ModelAdmin):
    """
    Отображение http-запроса в админке.
    """

    list_display = (
        "id",
        "project",
        "context",
        "type",
        "cwe",
        "detected_at",
    )
    list_display_links = ("id",)
    list_filter = (
        "type",
        "cwe",
    )
    search_fields = ("context","project",)
