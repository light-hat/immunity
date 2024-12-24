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

            return Response(
                Result.success(data={"contexts": context_list_prepared}).to_dict(),
                status=200
            )

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)
