"""
Модель HTTP-ответа.
"""

from django.db import models

from core.models.contexts import Context
from core.models.projects import Project


class Response(models.Model):
    """
    Модель ответа.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    status_code = models.CharField(max_length=255)
    headers = models.TextField()
    body = models.TextField()
    content_type = models.CharField(max_length=255)
    content_length = models.CharField(max_length=255, null=True, blank=True)
    charset = models.CharField(max_length=255, null=True, blank=True)
    version = models.CharField(max_length=255, null=True, blank=True)
    reason_phrase = models.CharField(max_length=255, null=True, blank=True)
    cookies = models.TextField()
    streaming = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Ответы"
        verbose_name = "Ответ"

    def __str__(self):
        return str(self.id)
