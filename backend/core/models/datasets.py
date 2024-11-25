"""
Модель для обучающего набора данных.
"""

import uuid

from django.db import models


class Dataset(models.Model):
    """
    Набор данных: тренировочный или валидационный.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10,
        choices=(
            ("learning", "Learning"),
            ("validation", "Validation"),
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Датасеты"
        verbose_name = "Датасет"

    def __str__(self):
        return str(self.name)
