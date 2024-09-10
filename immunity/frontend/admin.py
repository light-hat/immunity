"""
Настройки административной панели Django.
"""

from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.site_header = "Immunity IAST"
admin.site.site_title = "Администрирование Immunity IAST"
admin.site.index_title = "Добро пожаловать в административную панель Immunity IAST!"

admin.site.unregister(Group)
