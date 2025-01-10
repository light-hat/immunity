"""
Модель контекста выполнения запроса.
"""

from django.db import models

from core.models.projects import Project


class Library(models.Model):
    """
    Модель зависимости проекта.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.TextField()
    vulnerable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Зависимости проекта"
        verbose_name = "Зависимость проекта"

    def __str__(self):
        return str(self.id)
