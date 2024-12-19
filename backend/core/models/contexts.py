"""
Модель контекста выполнения запроса.
"""

from django.db import models

from core.models.projects import Project


class Context(models.Model):
    """
    Модель контекста.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    method = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Контексты выполнения"
        verbose_name = "Контекст выполнения"

    def __str__(self):
        return str(self.id)
