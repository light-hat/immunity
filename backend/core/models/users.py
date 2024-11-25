"""
Модель пользователя системы.
"""

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from core.cqrs.services.user_service import UserService


class User(AbstractUser):
    """
    Кастомная модель пользователя системы.
    """

    groups = models.ManyToManyField(
        Group, related_name="custom_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions", blank=True
    )
    role = models.CharField(
        max_length=13,
        verbose_name="Роль",
        choices=(
            ("admin", "Системный администратор"),
            ("analyst", "DevSecOps-аналитик"),
            ("data_engineer", "Инженер по разметке"),
        ),
    )

    objects = UserService()

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    def __str__(self):
        return str(self.username)
