"""
Модель приложения, для которого проводится интерактивный анализ.
"""

from django.db import models

from core.models.users import User


class Project(models.Model):
    """
    Модель анализируемого проекта.
    """

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
        return str(self.name)
