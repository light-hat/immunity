"""
Кастомная manage.py командп для инициализации системы при первом запуске.
"""

import logging

from django.core.management.base import BaseCommand

from core.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Запуск действий команды."""

        try:
            User.objects.get(username="admin")
            logger.info("Администратор уже создан.")
        except Exception:  # pylint: disable=bare-except
            User.objects.create_superuser(
                username="admin", email="admin@example.com", password="admin"
            )
