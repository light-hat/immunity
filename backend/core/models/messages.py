"""
Модель сообщения. Сущность сообщения описывает как запрос, так и ответ.
"""

import uuid

from django.db import models

from core.models.applications import Application
from core.models.contexts import Context


class Message(models.Model):
    """
    Унифицированная модель для запросов и ответов.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=10, choices=[("request", "Request"), ("response", "Response")]
    )
    method = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    headers = models.JSONField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    status_code = models.CharField(max_length=255, blank=True, null=True)
    cookies = models.JSONField(blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Сообщения"
        verbose_name = "Сообщение"

    def __str__(self):
        return str(self.id)
