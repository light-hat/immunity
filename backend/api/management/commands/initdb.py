"""
Инициализация системы при первом запуске.
"""

import logging

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Запуск действий команды."""

        try:
            Group.objects.get(name="Admins")
            logger.info("Группа администраторов уже создана.")
        except Exception:
            Group.objects.create(name="Admins")

        try:
            Group.objects.get(name="Users")
            logger.info("Группа пользователей уже создана.")
        except Exception:
            Group.objects.create(name="Users")

        try:
            User.objects.get(username="admin")
            logger.info("Администратор уже создан.")
        except Exception:
            admin_user = User.objects.create_superuser(
                username="admin", email="admin@example.com", password="admin"
            )
            admin_group = Group.objects.get(name="Admins")
            admin_user.groups.add(admin_group)
