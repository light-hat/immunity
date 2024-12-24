"""
Настройки бэкэнда для производственного окружения.
"""

import os
from os import environ

from django.core.management.utils import get_random_secret_key

from conf.settings.base import *  # pylint: disable=unused-wildcard-import

SECRET_KEY = get_random_secret_key()

DEBUG = True

HOST = environ.get("API_HOST")

PORT = environ.get("API_PORT")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "immunity",
    "db",
    HOST,
]

CSRF_TRUSTED_ORIGINS = [
    f"http://{HOST}:{PORT}",
]

CORS_ALLOWED_ORIGINS = [
    f"http://{HOST}:{PORT}",
    f"http://immunity:8000",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": environ.get("POSTGRES_DB"),
        "USER": environ.get("POSTGRES_USER"),
        "PASSWORD": environ.get("POSTGRES_PASSWORD"),
        "HOST": environ.get("POSTGRES_HOST"),
        "PORT": environ.get("POSTGRES_PORT", "5432"),
    }
}

# URL для доступа к статическим файлам
STATIC_URL = "/static/"

# Папка с подготовленными файлами фронта, из которой collectstatic заберёт статику
STATICFILES_DIRS = [BASE_DIR / "frontend_dist"]

# Путь для медиа-файлов
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
