"""
Configure Django admin.
"""

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

if settings.ENV == "dev":

    app_models = apps.get_app_config("api").get_models()

    for model in app_models:
        try:
            admin.site.register(model)
        except AlreadyRegistered:
            pass
