"""
Django settings for DEV environment.

This mode is specifically for development and debugging. Don't even think about using it in production.
"""

from config.settings import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["*"]

CORS_ALLOWED_ORIGINS = ["*"]

CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS += [
    "rest_framework",
    "rest_framework_simplejwt",
    "djoser",
    "drf_spectacular",
    "drf_spectacular_sidecar",
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

STATIC_URL = "/static/"

MEDIA_URL = "media/"
