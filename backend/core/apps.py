"""
Ядро серверной части. Описывает сущности БД и CQRS.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Ядро бэкэнда.
    Здесь описываются сущности БД и бизнес-логика.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        import core.admin  # pylint: disable=import-outside-toplevel
