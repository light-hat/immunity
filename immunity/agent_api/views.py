import base64
import json

from drf_spectacular.utils import OpenApiParameter, extend_schema
from engine.tasks import *
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class BaseApiView(viewsets.ViewSet):

    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # DEMO

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
    def upload(self, request, *args, **kwargs):
        """
        Метод загрузки отчёта от агента.
        """
        data = request.data
        try:
            # Получаем и расшифровываем строки из base64
            project_id = data["project"]
            decoded_request_data = base64.b64decode(data["request"]).decode("utf-8")
            decoded_control_flow = base64.b64decode(data["control_flow"]).decode(
                "utf-8"
            )
            decoded_response_data = base64.b64decode(data["response"]).decode("utf-8")

            # Десериализуем JSON
            json_request = json.loads(decoded_request_data)
            json_control_flow = json.loads(decoded_control_flow)
            json_response = json.loads(decoded_response_data)

            # Запускаем асинхронную задачу Celery
            task = handle_context.delay(
                project_id, json_request, json_control_flow, json_response
            )

        except (KeyError, ValueError, json.JSONDecodeError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "status": "success",
                "task_id": task.id,
            },
            status=status.HTTP_200_OK,
        )
