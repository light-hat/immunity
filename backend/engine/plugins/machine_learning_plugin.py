"""
Плагин для детектирования уязвимостей методами ML.
"""

import re
import ast
from typing import Any, Dict, List
import subprocess
import requests
import base64
from engine.plugins.base import BasePlugin

import logging
logger = logging.getLogger(__name__)


class MLPlugin(BasePlugin):
    """
    Плагин для обнаружения уязвимостей с помощью модели машинного обучения.
    """

    name = "machine_learning_plugin"
    description = "Ищет уязвимости в контексте выполнения запроса с помощью модели машинного обучения."

    def run(self, context_id: int, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Команда для запуска плагина.
        :param context_id: Идентификатор контекста.
        :param data: Данные контекста, преобразованные в словарь.
        :return: Список уязвимостей.
        """
        try:
            vulnerabilities = []
            logger.info("Запуск ML-модели для анализа контекста %s", str(context_id))

            encoded_data = base64.b64encode(str(data).encode('utf-8'))
            base64_data = encoded_data.decode('utf-8')

            result = subprocess.run(['python3', 'engine/infer_context_script.py', base64_data], capture_output=True, text=True)
            output = result.stdout.strip()
            if output:
                logger.warning(output)
            else:
                logger.error(result.stderr.strip())

            logger.info("Завершена ML-обработка для анализа контекста %s", str(context_id))

            # if any(cmd in body for cmd in dangerous_commands):
            #     vulnerabilities.append(
            #         {
            #             # "context_id": context_id,
            #             "type": "Command Injection",
            #             "cwe": "CWE-77",
            #             "description": f"Command '{cmd}' found in request body.",
            #             "evidence": body,
            #         }
            #     )

            return vulnerabilities
        except Exception as e:
            print(e)
