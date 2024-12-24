"""
Класс для предобработки контекста выполнения запроса.
"""

import ast
from typing import Any, Dict

from django.db.models import Q

from core.models import Event, Request, Response


class ContextHandler:
    """
    Класс для обработки контекста перед отправкой в движок.
    """

    @classmethod
    def handle(cls, context_object: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получает из БД объект контекста и формирует словарь с
        информацией, которая к нему привязана.
        :param context_object: Объект контекста.
        :return: Подготовленный словарь с данными о запросе,
        ответе и потоке управления.
        """

        request_object = Request.objects.filter(context=context_object).first()
        control_flow_objects = (
            Event.objects.filter(Q(context=context_object) & Q(type="code_execution"))
            .order_by("created_at")
            .values("code")
        )
        response_object = Response.objects.filter(context=context_object).first()

        return {
            "context_id": context_object.id,
            "vulnerable": context_object.vulnerable,
            "request": {
                "url": request_object.path,
                "method": request_object.method,
                "headers": ast.literal_eval(request_object.headers),
                "body": request_object.body,
            },
            "control_flow": {
                i: event["code"] for i, event in enumerate(control_flow_objects)
            },
            "response": {
                "status_code": response_object.status_code,
                "headers": ast.literal_eval(response_object.headers),
                #"body": response_object.body,
            },
        }
