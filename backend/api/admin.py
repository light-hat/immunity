"""
Настройки административной панели Django.
"""

from api.models import (User, Folder, File)
from django.contrib import admin
from django.contrib.auth.models import Group


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Отображение пользователя в админке.
    """
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active'
    )
    list_display_links = (
        "username",
    )
    list_filter = (
        'username',
        'email',
        'first_name',
        'last_name'
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_editable = (
        'is_staff',
        'is_active'
    )


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    """
    Отображение папки в админке.
    """
    list_display = (
        'name',
        'owner',
        'parent',
        'visible',
    )
    list_display_links = (
        "name",
    )
    list_filter = (
        'visible',
        'owner',
    )
    search_fields = (
        'name',
    )
    list_editable = (
        'visible',
    )


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """
    Отображение файла в админке.
    """
    list_display = (
        'filename',
        'extension',
        'owner',
        'folder',
        'type',
        'state',
        'visible',
        'size'
    )
    list_display_links = (
        "filename",
    )
    list_filter = (
        'type',
        'state',
        'visible',
        'owner',
    )
    search_fields = (
        'filename',
    )
    list_editable = (
        'visible',
    )


admin.site.unregister(Group)
