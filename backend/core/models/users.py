"""
Модель пользователя системы.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models


class UserManager(BaseUserManager):
    """
    Сервис пользователя.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и возвращает обычного пользователя с указанным email и паролем.
        """
        if not email:
            raise ValueError("Поле email обязательно для пользователя.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и возвращает суперпользователя с указанным email и паролем.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


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

    objects = UserManager()

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    def __str__(self):
        return str(self.username)
