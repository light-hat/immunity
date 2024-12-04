"""
Команда для обработки контекста выполнения запроса, присылаемого агентом.
"""

import base64
import json


class CreateContextCommand:
    """
    Команда для обработки контекста выполнения запроса, присылаемого агентом.
    """

    def __init__(
        self, project_id, request_base_64, control_flow_base_64, response_base_64
    ):
        """
        Конструктор команды.
        :param project_id: id анализируемого приложения.
        :param context_base_64: контекст выполнения запроса в формате base64.
        """
        self.project_id = project_id
        self.request_base_64 = request_base_64
        self.control_flow_base_64 = control_flow_base_64
        self.response_base_64 = response_base_64

    def execute(self):
        """
        Выполнение команды.
        """

        json_request = base64.b64decode(self.request_base_64).decode("utf-8")
        json_control_flow = base64.b64decode(self.control_flow_base_64).decode("utf-8")
        json_response = base64.b64decode(self.response_base_64).decode("utf-8")

        print(json_request)
        print("----------------------------------------")
