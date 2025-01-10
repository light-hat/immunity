"""
Отображение уязвимостей зависимостей.
"""

from django.contrib import admin

from core.models import DependencyVulnerability


@admin.register(DependencyVulnerability)
class DependencyVulnerabilityAdmin(admin.ModelAdmin):
    """
    Отображение зависимости проекта в админке.
    """

    list_display = (
        "id",
        "dependency",
        "label",
        "recommended_version",
        "detected_at",
    )
    list_display_links = ("label",)
