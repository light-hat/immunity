from django.contrib import admin
from user_api.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Отображение пользователя в админке.
    """

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_display_links = ("username",)
    list_filter = ("username", "email", "first_name", "last_name")
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
    list_editable = ("is_staff", "is_active")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Отображение приложения в админке.
    """

    list_display = (
        "id",
        "name",
        "language",
        "online",
        "created_at",
        "last_online",
    )
    list_display_links = ("id",)
    list_filter = (
        "language",
        "online",
    )
    search_fields = (
        "id",
        "name",
        "language",
        "online",
        "created_at",
        "last_online",
    )


@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    """
    Отображение контекста в админке.
    """

    list_display = (
        "id",
        "application",
        "created_at",
    )
    list_display_links = ("id",)
    list_filter = ("application",)
    search_fields = (
        "id",
        "application",
        "created_at",
    )


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    """
    Отображение запроса в админке.
    """

    list_display = (
        "id",
        "context",
        "method",
        "path",
    )
    list_display_links = ("id",)
    list_filter = ("context",)
    search_fields = (
        "id",
        "context",
        "method",
        "path",
    )


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    """
    Отображение ответа в админке.
    """

    list_display = (
        "id",
        "status_code",
        "content_type",
        "content_length",
        "reason_phrase",
    )
    list_display_links = ("id",)
    list_filter = (
        "status_code",
        "content_type",
        "content_length",
    )
    search_fields = (
        "id",
        "status_code",
        "content_type",
        "content_length",
        "reason_phrase",
    )


admin.site.register(ControlFlow)
admin.site.register(FunctionCall)
admin.site.register(CodeExecution)
admin.site.register(ReturnFunction)
admin.site.register(Error)
