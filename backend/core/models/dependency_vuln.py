"""
Модель для уязвимостей библиотек.
"""

from django.db import models

from core.models import Library


class DependencyVulnerability(models.Model):
    """
    Модель для найденных уязвимостей в анализируемых зависимостях.
    """

    dependency = models.ForeignKey(Library, on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    recommended_version = models.CharField(max_length=500)
    detected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-detected_at"]
        verbose_name_plural = "Уязвимости библиотек"
        verbose_name = "Уязвимость библиотеки"

    def __str__(self):
        return f"{self.label})"
