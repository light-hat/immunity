"""
Подключаем Celery к Django-бэкэнду.
"""

import os
from celery import Celery #pylint: disable=wrong-import-position

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
celery_app = Celery('core')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
