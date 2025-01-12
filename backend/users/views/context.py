"""
API эндпоинты для проектов.
"""

import logging
import ast
from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
import rest_framework.response

from core.command import Command
from core.models import *
from core.query import Query
from core.result import Result
from engine.handler import ContextHandler

from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


class ContextAPIView(viewsets.ViewSet):
    """
    API для работы с уязвимостями.
    """

    # permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="project",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Проект",
            ),
        ],
        tags=["context"],
    )
    def filter(self, request):
        """
        Фильтрация объектов.
        """
        try:

            filters = {
                "project": request.GET.get("project"),
                #"page": request.GET.get("page"),
                #"page_size": request.GET.get("page_size"),
            }

            project = Project.objects.get(pk=int(filters["project"]))
            contexts = Context.objects.filter(project=project)
            context_list_prepared = [
                ContextHandler.handle(context)
                for context in contexts
            ]

            return rest_framework.response.Response(
                Result.success(data={"contexts": context_list_prepared}).to_dict(),
                status=200
            )

        except Exception as e:
            logger.error(e)
            return rest_framework.response.Response(Result(e).to_dict(), status=500)


class ContextDetailAPIView(viewsets.ViewSet):
    """
    API-метод для получения контекста по ID.
    """

    def retrieve(self, request, pk=None):
        """
        Получение данных по ID родительской модели.
        """

        context = get_object_or_404(Context, pk=pk)

        request = Request.objects.get(context=context)
        response = Response.objects.get(context=context)
        events = Event.objects.filter(context=context)
        vulns = Vulnerability.objects.filter(context=context)
        data = {
            "context": {
                "id": context.id,
                "vulnerable": context.vulnerable,
                "created_at": context.created_at
            },
            "request": {
                "id": request.id,
                "method": request.method,
                "path": request.path,
                "body": request.body if request.body != "b''" else "",
                "headers": ast.literal_eval(request.headers),
                "user": request.user,
                "get_params": request.get_params,
                "post_params": request.post_params,
                "cookies": request.cookies,
                "files": request.files,
                "meta": request.meta,
            },
            "response": {
                "id": response.id,
                "status_code": response.status_code,
                "headers": ast.literal_eval(response.headers),
                "body": response.body,
                "content_type": response.content_type,
                "content_length": response.content_length,
                "charset": response.charset,
                "version": response.version,
                "reason_phrase": response.reason_phrase,
                "cookies": response.cookies,
                "streaming": response.streaming,
            },
            "events": [],
            "vulns": [],
            "event_types": {
                "function_call": "Вызов функции",
                "code_execution": "Выполнение кода",
                "return_function": "Возврат из функции",
                "error": "Исключение",
            }
        }

        for event in events:
            data["events"].append({
                "id": event.id,
                "timestamp": event.timestamp,
                "type": event.type,
                "external_call": event.external_call,
                "func_name": event.func_name,
                "module": event.module,
                "filename": event.filename,
                "line": event.line,
                "args": event.args, #[ast.literal_eval(x) for x in ast.literal_eval(event.args)],
                "code": event.code,
                "exception_type": event.exception_type,
                "exception_message": event.exception_message,
            })

        for vuln in vulns:
            data["vulns"].append({
                "type": vuln.type,
                "cwe": vuln.cwe,
                "description": vuln.description,
            })

        return rest_framework.response.Response(data, status=status.HTTP_200_OK)
