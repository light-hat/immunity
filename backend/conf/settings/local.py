"""
Настройки бэкэнда для локального запуска.
"""

from conf.settings.base import *  # pylint: disable=unused-wildcard-import
from django.core.management.utils import get_random_secret_key

SECRET_KEY = get_random_secret_key()

DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "/static/"

MEDIA_URL = "media/"
