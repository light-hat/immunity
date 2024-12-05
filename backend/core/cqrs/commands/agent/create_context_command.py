"""
Команда для обработки контекста выполнения запроса, присылаемого агентом.
"""

from core.result import Result
from engine.agent.context import handle_context


class CreateContextCommand:
    """
    Команда для обработки контекста выполнения запроса, присылаемого агентом.
    """

    def __init__(
        self, project_id, request, control_flow, response
    ):
        """
        Конструктор команды.
        :param project_id: id анализируемого приложения.
        :param context: контекст выполнения запроса.
        :param control_flow: потом управления.
        :param response: ответ на запрос.
        """
        self.project_id = project_id
        self.request = request
        self.control_flow = control_flow
        self.response = response

    def execute(self):
        """
        Выполнение команды.
        """

        task = handle_context.delay(
            self.project_id, self.request, self.control_flow, self.response
        )

        return Result.success(data={"task_id": task.id})
