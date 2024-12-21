"""
Модель для найденной уязвимости.
"""

from django.db import models

from core.models.contexts import Context
from core.models.projects import Project


class Vulnerability(models.Model):
    """
    Модель для найденной уязвимости в анализируемом приложении.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    cwe = models.CharField(max_length=50)
    description = models.TextField()
    evidence = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-detected_at"]
        verbose_name_plural = "Уязвимости"
        verbose_name = "Уязвимость"

    def __str__(self):
        return f"{self.type} (Context: {self.context})"
