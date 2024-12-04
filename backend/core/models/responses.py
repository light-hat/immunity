"""
Модель HTTP-ответа.
"""

import uuid

from core.models.applications import Application
from core.models.contexts import Context
from django.db import models


class Response(models.Model):
    """
    Модель ответа.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    status_code = models.CharField(max_length=255)
    headers = models.TextField()
    body = models.TextField()
    content_type = models.CharField(max_length=255)
    content_length = models.CharField(max_length=255)
    charset = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    reason_phrase = models.CharField(max_length=255)
    cookies = models.TextField()
    streaming = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Ответы"
        verbose_name = "Ответ"

    def __str__(self):
        return str(self.id)
