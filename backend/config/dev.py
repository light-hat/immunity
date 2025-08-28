"""
Django settings for DEV environment.

This mode is specifically for development and debugging. Don't even think about using it in production.
"""

import os
from datetime import timedelta
from os import environ

from config.settings import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["http://87.228.88.155:8000", "http://87.228.88.155"]

CORS_ALLOWED_ORIGINS = ["http://87.228.88.155:8000", "http://87.228.88.155"]

CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS += [
    "rest_framework",
    "rest_framework_simplejwt",
    "djoser",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # "debug_toolbar",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    *MIDDLEWARE,
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    # Cookie settings for refresh tokens
    "REFRESH_TOKEN_COOKIE_NAME": "refresh_token",
    "REFRESH_TOKEN_COOKIE_HTTPONLY": True,
    "REFRESH_TOKEN_COOKIE_SECURE": True,  # Set to True for security
    "REFRESH_TOKEN_COOKIE_SAMESITE": "Lax",
    "REFRESH_TOKEN_COOKIE_PATH": "/",
}

DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "#/password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "#/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": False,
    "SERIALIZERS": {
        "user": "api.serializers.CustomUserSerializer",
        "current_user": "api.serializers.CustomUserSerializer",
    },
}

# DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}


# def show_toolbar(request):
#     return True


# SHOW_TOOLBAR_CALLBACK = show_toolbar

# INTERNAL_IPS = [
#     "127.0.0.1",
#     str(environ.get("DEV_HOSTNAME")),
# ]

# DEBUG_TOOLBAR_PANELS = [
#     "debug_toolbar.panels.history.HistoryPanel",
#     "debug_toolbar.panels.versions.VersionsPanel",
#     "debug_toolbar.panels.timer.TimerPanel",
#     "debug_toolbar.panels.settings.SettingsPanel",
#     "debug_toolbar.panels.headers.HeadersPanel",
#     "debug_toolbar.panels.request.RequestPanel",
#     "debug_toolbar.panels.sql.SQLPanel",
#     "debug_toolbar.panels.staticfiles.StaticFilesPanel",
#     "debug_toolbar.panels.templates.TemplatesPanel",
#     "debug_toolbar.panels.alerts.AlertsPanel",
#     "debug_toolbar.panels.cache.CachePanel",
#     "debug_toolbar.panels.signals.SignalsPanel",
#     "debug_toolbar.panels.redirects.RedirectsPanel",
#     "debug_toolbar.panels.profiling.ProfilingPanel",
# ]

# DEBUG_TOOLBAR_CONFIG = {
#     "RESULTS_CACHE_SIZE": 3,
#     "SHOW_COLLAPSED": False,
#     "SQL_WARNING_THRESHOLD": 100,
# }

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - [%(levelname)s] - [%(threadName)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
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
            "level": "INFO",
            "propagate": True,
        },
        "celery": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "core": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "api": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "communication": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
