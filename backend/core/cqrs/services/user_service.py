"""
Модуль для описания бизнес-логики пользователя.
"""

from django.contrib.auth.models import BaseUserManager


class UserService(BaseUserManager):
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
