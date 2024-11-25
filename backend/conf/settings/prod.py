"""
Настройки бэкэнда для производственного окружения.
"""

from .base import *
import os
from os import environ
from django.core.management.utils import get_random_secret_key


SECRET_KEY = get_random_secret_key()

DEBUG = False

HOST = environ.get("API_URL")

PORT = environ.get("API_PORT")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "db",
    HOST,
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    f"http://{HOST}:{PORT}",
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

STATIC_URL = "static/"
STATIC_DIR = os.path.join(BASE_DIR, "static")
STATIC_ROOT = STATIC_DIR

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
