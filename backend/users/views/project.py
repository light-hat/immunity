"""
API эндпоинты для проектов.
"""

import logging

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.command import Command
from core.models import Project
from core.query import Query
from core.result import Result

logger = logging.getLogger(__name__)


class ProjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=None)
    language = serializers.CharField(max_length=255)


class ProjectAPIView(viewsets.ViewSet):
    """
    API для работы с проектами.
    """

    # permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(description="Список проектов"),
            400: OpenApiResponse(description="Некорректный запрос"),
            500: OpenApiResponse(description="Внутренняя ошибка сервера"),
        },
        methods=["GET"],
        tags=["project"],
    )
    def get(self, request):
        """Получение всех объектов."""

        try:
            query = Query(model=Project)
            result = query.all()

            if result.is_success:
                return Response(result.to_dict(), status=200)
            else:
                return Response(result.to_dict(), status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Поиск по пользователю",
            ),
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Поиск по названию",
            ),
            OpenApiParameter(
                name="language",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Поиск по языку программирования",
            ),
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Страница пагинации",
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Количество объектов на странице пагинации",
            ),
        ],
        tags=["project"],
    )
    def filter(self, request):
        """Фильтрация объектов."""
        try:

            filters = {
                "user": request.GET.get("user"),
                "name": request.GET.get("name"),
                "language": request.GET.get("language"),
                "page": request.GET.get("page"),
                "page_size": request.GET.get("page_size"),
            }

            query = Query(model=Project)
            result = query.filter(
                filters={
                    "user__id": filters["user"],
                    "name": filters["name"],
                    "language": filters["language"],
                },
                pagination={
                    "page": int(filters["page"]) if filters["page"] is not None else 1,
                    "page_size": (
                        int(filters["page_size"])
                        if filters["page_size"] is not None
                        else 10
                    ),
                },
            )

            if result.is_success:
                return Response(result.to_dict(), status=200)
            else:
                return Response(result.to_dict(), status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            200: OpenApiResponse(description="Данные о проекте"),
            404: OpenApiResponse(description="Проект не найден"),
        },
        methods=["GET"],
        tags=["project"],
    )
    def retrieve(self, request, pk):
        """Получение объекта по ID"""
        try:
            query = Query(model=Project)
            result = query.get_by_id(pk)

            if result.is_success:
                return Response(result.to_dict(), status=200)
            else:
                return Response(result.to_dict(), status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)

    @extend_schema(
        request=ProjectSerializer,
        responses={
            201: OpenApiResponse(description="Проект успешно создан"),
            400: OpenApiResponse(description="Ошибка валидации данных"),
        },
        methods=["POST"],
        tags=["project"],
    )
    def post(self, request):
        """Создание нового объекта."""

        try:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                command = Command(model=Project, data=data)
                result = command.create()

                if result.is_success:
                    return Response(result.to_dict(), status=201)
                else:
                    return Response(result.to_dict(), status=400)
            return Response(serializer.errors, status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH
            ),
        ],
        request=ProjectSerializer,
        responses={
            200: OpenApiResponse(description="Проект успешно изменён"),
            400: OpenApiResponse(description="Ошибка валидации данных"),
            404: OpenApiResponse(description="Проект не найден"),
        },
        methods=["PUT"],
        tags=["project"],
    )
    def put(self, request, pk):
        """Обновление объекта."""

        try:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                command = Command(
                    model=Project,
                    entity_id=pk,
                    data=data,
                    foreign_keys={"user": self.request.user.id},
                )
                result = command.update()

                if result.is_success:
                    return Response(result.to_dict(), status=200)
                else:
                    return Response(result.to_dict(), status=400)
            return Response(serializer.errors, status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id", type=OpenApiTypes.INT, location=OpenApiParameter.PATH
            ),
        ],
        responses={
            204: OpenApiResponse(description="Проект успешно удалён"),
            404: OpenApiResponse(description="Проект не найден"),
        },
        methods=["DELETE"],
        tags=["project"],
    )
    def delete(self, request, pk):
        """Удаление объекта."""

        try:
            command = Command(model=Project, entity_id=pk)
            result = command.delete()

            if result.is_success:
                return Response(result.to_dict(), status=204)
            else:
                return Response(result.to_dict(), status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)
