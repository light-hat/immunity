"""
API эндпоинты для проектов.
"""

import logging

from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.command import Command
from core.models import Context, DatasetLabel, Event, Project
from core.query import Query
from core.result import Result
from engine.handler import ContextHandler

logger = logging.getLogger(__name__)


class MarkupSerializer(serializers.Serializer):
    project = serializers.IntegerField()
    label = serializers.CharField(max_length=10)
    file = serializers.CharField(max_length=None)
    line = serializers.IntegerField()


class DatasetAPIView(viewsets.ViewSet):
    """
    API для работы с уязвимостями.
    """

    # permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
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
        tags=["dataset"],
    )
    def filter(self, request):
        """Фильтрация объектов."""
        try:

            filters = {
                "page": request.GET.get("page"),
                "page_size": request.GET.get("page_size"),
            }

            query = Query(model=DatasetLabel)
            result = query.filter(
                filters={},
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
        request=MarkupSerializer,
        responses={
            201: OpenApiResponse(description="Уязвимые контексты размечены"),
            400: OpenApiResponse(description="Ошибка валидации данных"),
        },
        methods=["POST"],
        tags=["dataset"],
    )
    def post(self, request):
        """
        Разметка датасета.
        На вход подаются данные из отчетов стат анализа,
        :param request: На входе - результаты статического анализа,
        где находятся уязвимые участки кода.
        :return: На выходе - что было размечено.
        """

        try:
            serializer = MarkupSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data

                project = Project.objects.get(pk=data["project"])
                label = data["label"]
                file = data["file"]
                line = data["line"]

                vulnerable_events = Event.objects.filter(
                    Q(line=line)
                    & Q(filename=file)
                    & Q(project=project)
                    & Q(type="code_execution")
                ).distinct()

                filtered_contexts = vulnerable_events.values_list(
                    "context", flat=True
                ).distinct()

                contexts_prepared = [
                    ContextHandler.handle(Context.objects.get(id=context))
                    for context in filtered_contexts
                ]

                for c in contexts_prepared:
                    DatasetLabel.objects.create(text=c, label=label)

                return Response(
                    Result.success(data={"contexts": contexts_prepared}).to_dict(),
                    status=200,
                )
            return Response(serializer.errors, status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)
