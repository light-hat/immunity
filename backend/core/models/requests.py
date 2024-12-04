"""
Модель HTTP-запроса.
"""

import uuid

from core.models.applications import Application
from core.models.contexts import Context
from django.db import models


class Request(models.Model):
    """
    Модель запроса.
    Содержит данные об обработанном запросе и является частью контекста.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    method = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    body = models.TextField()
    headers = models.TextField()
    user = models.CharField(max_length=255)
    get_params = models.TextField()
    post_params = models.TextField()
    cookies = models.TextField()
    files = models.TextField()
    meta = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Запросы"
        verbose_name = "Запрос"

    def __str__(self):
        return str(self.id)
