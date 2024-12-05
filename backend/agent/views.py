"""
Модуль для реализации API, предназначенного для взаимодействия
с агентами интерактивного анализа.

Этот модуль предоставляет следующие возможности:
- Отправка контекста выполнения запроса.
"""

import base64
import json

from core.cqrs.commands.agent.create_context_command import CreateContextCommand
from core.models import Application
from core.result import Result
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class ContextSerializer(serializers.Serializer):
    """Сериализатор для приема контекста выполнения запроса.

    Атрибуты:
        project (CharField): Название приложения.
        request (TextField): Запрос.
        control_flow (TextField): Поток управления.
        response (TextField): Ответ.
    """

    def validate_project(self, value):  # TODO: DRY REFACTOR
        if not value:
            raise ValidationError("Параметр project не может быть пустым.")
        try:
            Application.objects.get(name=value)
        except Application.DoesNotExist:
            raise ValidationError("Приложение с названием {} не найдено.".format(value))
        return value

    def validate_request(self, value):  # TODO: DRY REFACTOR
        try:
            base64.b64decode(value).decode("utf-8")
        except:
            raise ValidationError("Параметр request должен быть закодирован в Base64.")
        return value

    def validate_control_flow(self, value):  # TODO: DRY REFACTOR
        try:
            base64.b64decode(value).decode("utf-8")
        except:
            raise ValidationError(
                "Параметр control_flow должен быть закодирован в Base64."
            )
        return value

    def validate_response(self, value):  # TODO: DRY REFACTOR
        try:
            base64.b64decode(value).decode("utf-8")
        except:
            raise ValidationError("Параметр response должен быть закодирован в Base64.")
        return value

    project = serializers.CharField(max_length=255)
    request = serializers.CharField(max_length=None)
    control_flow = serializers.CharField(max_length=None)
    response = serializers.CharField(max_length=None)


class ContextAPIViewset(viewsets.ViewSet):
    """
    APIView для приема контекста выполнения запроса.

    Методы:
    - POST: Добавить контекст выполнения запроса.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        request=ContextSerializer,
        responses={
            200: OpenApiResponse(
                description="Успешный ответ.",
                response=Result.success().to_dict(),
                examples=[
                    OpenApiExample(
                        "Успешный ответ",
                        value=Result.success().to_dict(),
                        request_only=False,
                        response_only=True,
                    ),
                ],
            ),
            400: OpenApiResponse(
                description="Сообщение о пользовательской ошибке.",
                response=Result.failure(errors="Сообщение об ошибке.").to_dict(),
                examples=[
                    OpenApiExample(
                        "Некорректный запрос",
                        value=Result.failure(
                            errors={
                                "Параметр": "Сообщение об ошибке.",
                            }
                        ).to_dict(),
                        request_only=False,
                        response_only=True,
                    ),
                ],
            ),
            500: OpenApiResponse(
                description="Сообщение о внутренней ошибке.",
                response=Result.failure(
                    errors="Сообщение о внутренней ошибке."
                ).to_dict(),
                examples=[
                    OpenApiExample(
                        "Внутренняя ошибка сервера",
                        value=Result.failure(
                            errors="Сообщение об ошибке.",
                            meta={
                                "exception_type": "Класс исключения",
                            },
                        ).to_dict(),
                        request_only=False,
                        response_only=True,
                    ),
                    OpenApiExample(
                        "Внутренняя ошибка сервера (режим отладки)",
                        value=Result.failure(
                            errors="Сообщение об ошибке.",
                            meta={
                                "exception_type": "Класс исключения",
                                "traceback": ["Трассировка ошибки"],
                            },
                        ).to_dict(),
                        request_only=False,
                        response_only=True,
                    ),
                ],
            ),
        },
        summary="Добавить контекст выполнения запроса.",
        description="Принимает три строки в base64, расшифровывает их и передает в асинхронную Celery задачу.",
        tags=["agent"],
    )
    def post(self, request, *args, **kwargs) -> Response:
        """
        Добавить контекст выполнения запроса.

        Параметры:
            request (Request): Объект HTTP-запроса с JSON-данными контекста.

        Возвращает:
            Response: JSON-объект с подтверждением или сообщением об ошибке.
        """
        serializer = ContextSerializer(data=request.data)

        if serializer.is_valid():
            try:
                data = serializer.validated_data

                command = CreateContextCommand(
                    data["project"],
                    json.loads(base64.b64decode(data["request"]).decode("utf-8")),
                    json.loads(base64.b64decode(data["control_flow"]).decode("utf-8")),
                    json.loads(base64.b64decode(data["response"]).decode("utf-8")),
                )
                result = command.execute()

                return Response(result.to_dict(), status=200)
            except Exception as e:
                return Response(Result(e).to_dict(), status=500)
        else:
            return Response(Result.failure(serializer.errors).to_dict(), status=400)
