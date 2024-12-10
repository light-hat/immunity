"""
Модуль, описывающий запросы для сущности пользователя.
"""

from core.models import User


class UserQuery:
    """
    Запросы для получения пользователей.
    """

    @staticmethod
    def get_by_id(user_id: int) -> dict:
        """
        Получает объект пользователя по id.
        :param user_id: ID пользователя в базе данных.
        :return: Словарь с полями пользователя, либо пустое значение.
        """

        user = User.objects.filter(id=user_id).first()
        if not user:
            return None
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
