"""
Модель приложения, для которого проводится интерактивный анализ.
"""

import uuid

from django.db import models

from core.models.users import User


class Application(models.Model):
    """
    Модель анализируемого приложения.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=255, choices=(("python", "Python"),))
    online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Приложения"
        verbose_name = "Приложение"

    def __str__(self):
        return self.name
