"""
Тестовый обработчик для графа.
"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class GraphDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):  # pylint: disable=unused-argument
        """
        Тестовый обработчик для графа.
        """
        data = {
            "nodes": [
                {
                    "id": "1",
                    "type": "input",
                    "label": "Node 1",
                    "position": {"x": 250, "y": 5},
                },
                {
                    "id": "2",
                    "type": "output",
                    "label": "Node 2",
                    "position": {"x": 100, "y": 100},
                },
                {
                    "id": "3",
                    "type": "custom",
                    "label": "Node 3",
                    "position": {"x": 400, "y": 100},
                },
            ],
            "edges": [
                {"id": "e1-2", "source": "1", "target": "2", "type": "custom"},
                {"id": "e1-3", "source": "1", "target": "3", "animated": "true"},
            ],
        }
        return Response(data)
