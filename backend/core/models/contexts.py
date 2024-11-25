"""
Модель контекста выполнения запроса.
"""

import uuid

from django.db import models

from core.models.applications import Application


class Context(models.Model):
    """
    Модель контекста.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Контексты выполнения"
        verbose_name = "Контекст выполнения"

    def __str__(self):
        return str(self.id)
