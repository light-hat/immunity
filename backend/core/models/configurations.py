"""
Модель контекста выполнения запроса.
"""

from django.db import models

from core.models.projects import Project


class Configuration(models.Model):
    """
    Модель конфигурации проекта.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.TextField()
    vulnerable = models.BooleanField(default=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Конфигурации"
        verbose_name = "Конфигурация"

    def __str__(self):
        return str(self.key)
