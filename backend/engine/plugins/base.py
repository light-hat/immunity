"""
Базовый плагин движка интерактивного анализа.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BasePlugin(ABC):
    """
    Базовый класс для всех плагинов анализа.
    Каждый плагин должен реализовать метод `run`.
    """

    name: str = "base_plugin"
    description: str = "Base plugin for vulnerability detection."

    @abstractmethod
    def run(self, context_id: int, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Запуск плагина.

        :param context_id: Идентификатор контекста.
        :param data: Словарь данных (запрос, ответ, поток управления).
        :return: Список обнаруженных уязвимостей.
        """
        pass
