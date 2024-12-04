"""
Модель метки обучающего набора данных.
"""

import uuid

from core.models.datasets import Dataset
from django.db import models


class DatasetLabel(models.Model):
    """
    Метка для обучающего набора.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    token_labels = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Метки датасетов"
        verbose_name = "Метка датасета"

    def __str__(self):
        return str(self.id)
