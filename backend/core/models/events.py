"""
Модель для событий потока управления.
"""

from django.db import models

from core.models.contexts import Context
from core.models.projects import Project


class Event(models.Model):
    """
    Унифицированная модель для событий потока управления.
    """

    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
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
    external_call = models.BooleanField(default=False)
    func_name = models.CharField(max_length=255, blank=True, null=True)
    module = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    line = models.IntegerField(blank=True, null=True)
    args = models.JSONField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    exception_type = models.CharField(max_length=255, blank=True, null=True)
    exception_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "События"
        verbose_name = "Событие"

    def __str__(self):
        return f"{self.project.name} - {self.type}"
