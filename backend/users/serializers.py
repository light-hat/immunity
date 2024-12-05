"""
Модуль содержит сериализаторы для кастомной модели пользователя.
"""

from typing import Any, Dict  # Типы для аннотаций

from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from core.models import User


class UserCreateSerializer(BaseUserRegistrationSerializer):
    """
    Сериализатор для создания новых пользователей.
    Наследуется от стандартного UserCreateSerializer из Djoser.
    Используется для кастомизации процесса регистрации пользователей.
    """

    class Meta(BaseUserRegistrationSerializer.Meta):
        """
        Мета-класс для определения параметров сериализатора.
        Определяет модель пользователя и поля, которые будут доступны.
        """
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

    def create(self, validated_data: Dict[str, Any]) -> User:
        """
        Метод создания нового пользователя.
        Переопределяется для использования метода родительского класса.

        :param validated_data: Проверенные данные, полученные из запроса.
        :return: Новый объект пользователя.
        """
        user = super().create(validated_data)
        return user
