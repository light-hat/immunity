"""
Модель для событий потока управления.
"""

import uuid

from django.db import models

from core.models.applications import Application
from core.models.contexts import Context


class Event(models.Model):
    """
    Унифицированная модель для событий потока управления.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    type = models.CharField(
        max_length=20,
        choices=[
            ("function_call", "Function Call"),
            ("code_execution", "Code Execution"),
            ("return_function", "Return Function"),
            ("error", "Error"),
        ],
    )
    func_name = models.CharField(max_length=255, blank=True, null=True)
    module = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    line = models.IntegerField(blank=True, null=True)
    args = models.JSONField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    final_state = models.JSONField(blank=True, null=True)
    returned_value = models.JSONField(blank=True, null=True)
    exception_type = models.CharField(max_length=255, blank=True, null=True)
    exception_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "События"
        verbose_name = "Событие"

    def __str__(self):
        return f"{self.application.name} - {self.type}"
