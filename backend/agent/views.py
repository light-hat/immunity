"""
Модуль для реализации API, предназначенного для взаимодействия
с агентами интерактивного анализа.

Этот модуль предоставляет следующие возможности:
- Отправка контекста выполнения запроса.
"""

from core.cqrs.commands.create_context_command import CreateContextCommand
from django.http import JsonResponse
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


class ContextAPIViewset(viewsets.ViewSet):
    """
    APIView для приема контекста выполнения запроса.

    Методы:
    - POST: Добавить контекст выполнения запроса.
    """

    permission_classes = [AllowAny]

    @action(methods=["post"], detail=False)
    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "request": {"type": "string"},
                    "control_flow": {"type": "string"},
                    "response": {"type": "string"},
                },
            }
        },
        responses={
            200: OpenApiParameter(name="Success", type="string"),
            400: OpenApiParameter(name="Error", type="string"),
        },
        description="Принимает три строки в base64, расшифровывает их и передает в асинхронную Celery задачу.",
    )
    def post(self, request, *args, **kwargs) -> JsonResponse:
        """
        Добавить контекст выполнения запроса.

        Параметры:
            request (Request): Объект HTTP-запроса с JSON-данными контекста.

        Возвращает:
            Response: JSON-объект с подтверждением или сообщением об ошибке.
        """
        data: Dict[str, str] = request.data

        command = CreateContextCommand(
            project=data["project"],
            request=data["request"],
            control_flow=data["control_flow"],
            response=data["response"],
        )
        result = command.execute()

        return JsonResponse(result.to_dict(), status=200 if result.success else 400)
