"""
Модель HTTP-запроса.
"""

from django.db import models

from core.models.contexts import Context
from core.models.projects import Project


class Request(models.Model):
    """
    Модель запроса.
    Содержит данные об обработанном запросе и является частью контекста.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
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
