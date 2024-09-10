import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя системы.
    """
    phone_number = models.CharField(max_length=15, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    def __str__(self):
        return str(self.username)
