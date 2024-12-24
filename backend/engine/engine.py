"""
Модуль движка интерактивного анализа.

Входными данными является контекст обработки запроса анализируемого приложения.
На выходе создаются объекты уязвимостей в базе данных.
Функциональность движка реализуется через плагины.
"""

import importlib
import logging
import os
from typing import Any, Dict, List

from celery import shared_task

from core.models import Context, Project, Vulnerability
from engine.plugins.base import BasePlugin

logger = logging.getLogger(__name__)


@shared_task
def run_analysis_task(project_id: int, context_id: int, data: Dict[str, Any]):
    """
    Celery-задача для запуска движка интерактивного анализа.
    """
    logger.info("Обработка движком контекста %s проекта %s", context_id, project_id)
    engine = IASTEngine()
    engine.run_analysis(project_id, context_id, data)
    logger.info(
        "Завершена обработка движком контекста %s проекта %s", context_id, project_id
    )


class IASTEngine:
    """
    Движок для выполнения анализа с использованием плагинов.
    """

    def __init__(self):
        self.plugins = self.load_plugins()

    def load_plugins(self) -> List:
        """
        Загружает все плагины из каталога plugins.
        """
        plugins = []
        plugin_dir = os.path.dirname(__file__) + "/plugins"

        for filename in os.listdir(plugin_dir):
            if filename.endswith("_plugin.py") and filename != "base.py":
                module_name = f"engine.plugins.{filename[:-3]}"
                module = importlib.import_module(module_name)

                for attr in dir(module):
                    cls = getattr(module, attr)
                    if (
                        isinstance(cls, type)
                        and issubclass(cls, BasePlugin)
                        and cls != BasePlugin
                    ):
                        plugins.append(cls())
        return plugins

    def run_analysis(self, project: int, context: int, data: Dict[str, Any]):
        """
        Запускает анализ с использованием всех плагинов.
        """
        try:
            vulnerabilities = []
            for plugin in self.plugins:
                vulnerabilities.extend(plugin.run(context, data))

            # Сохраняем уязвимости в БД
            for vuln in vulnerabilities:
                Vulnerability.objects.create(
                    project=Project.objects.get(id=project),
                    context=Context.objects.get(id=context),
                    type=vuln["type"],
                    cwe=vuln["cwe"],
                    description=vuln["description"],
                    evidence=vuln["evidence"],
                )

            # Помечаем контекст как уязвимый
            if len(vulnerabilities) > 0:
                context = Context.objects.get(id=context)
                context.vulnerable = True
                context.save()

            return vulnerabilities

        except Exception as e:
            logger.error(e)
