"""
Базовые настройки проекта бэкэнда.
"""

import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

AUTH_USER_MODEL = "core.User"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "djoser",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "core",
    "agent",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DATETIME_FORMAT": "%d.%m.%Y %H:%M",
    "DATE_FORMAT": "%d.%m.%Y",
    "TIME_FORMAT": "%H:%M",
    # "DEFAULT_PERMISSION_CLASSES": [
    #    "rest_framework.permissions.IsAuthenticated",
    # ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

DATETIME_FORMAT = "%d.%m.%Y %H:%M"

DATE_FORMAT = "%d.%m.%Y"

TIME_FORMAT = "%H:%M"

DJOSER = {
    "LOGIN_FIELD": "username",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SERIALIZERS": {
        #'user_create': 'users.serializers.UserCreateSerializer',
        #'current_user': 'rest_framework.serializers.CurrentUserSerializer',
        "user_create": "djoser.serializers.UserCreateSerializer",
        "user": "djoser.serializers.UserSerializer",
    },
    "TOKEN_MODEL": None,
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}


SPECTACULAR_SETTINGS = {
    "TITLE": "Immunity IAST API",
    "DESCRIPTION": "Программный интерфейс для взаимодействия с управляющим сервером Immunity IAST.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

ROOT_URLCONF = "conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - [%(levelname)s] - [%(threadName)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",  # pylint: disable=line-too-long
            "style": "%",
        },
        "simple": {
            "format": "[%(levelname)s] %(message)s",
            "style": "%",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "core": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "agent": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "users": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "engine": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

WSGI_APPLICATION = "conf.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
