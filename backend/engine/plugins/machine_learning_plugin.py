"""
Плагин для детектирования CWE-77.
"""

import re
import ast
from typing import Any, Dict, List

import torch
import json
import requests
from transformers import AutoTokenizer

from engine.plugins.base import BasePlugin
from engine.model import IAST_BERT
import logging
logger = logging.getLogger(__name__)


if torch.cuda.is_available():
    logger.info(f"GPU доступен: {torch.cuda.get_device_name(0)}")
else:
    logger.info("GPU недоступен, используется CPU")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

id2label = {'CWE-352': 0, 'CWE-502': 1, 'CWE-77': 2, 'CWE-79': 3, 'CWE-89': 4}

# Укажите репозиторий
repo_id = "l1ghth4t/immunity"

# Загрузка конфигурации
config_path = f"https://huggingface.co/{repo_id}/resolve/main/config.json"
config = json.loads(requests.get(config_path).text)

# Инициализация модели
model = IAST_BERT(
    bert_model_name=config["bert_model_name"],
    num_classes=11
)

# Загрузка весов
state_dict_path = f"https://huggingface.co/{repo_id}/resolve/main/pytorch_model.bin"
state_dict = torch.hub.load_state_dict_from_url(state_dict_path, map_location=device)
model.load_state_dict(state_dict)

# Загрузка токенизатора
tokenizer = AutoTokenizer.from_pretrained(repo_id)

# Модель готова
model.eval()

class MLPlugin(BasePlugin):
    """
    Плагин для обнаружения уязвимостей с помощью модели машинного обучения.
    """

    name = "machine_learning_plugin"
    description = "Ищет уязвимости в контексте выполнения запроса с помощью модели машинного обучения."

    def preprocess_context(self, json_example):
        # Обработка блока Request
        request_text = f"URL: {json_example['request']['url']}\n" \
                       f"Method: {json_example['request']['method']}\n" \
                       f"Headers: {json_example['request']['headers']}\n" \
                       f"Body: {json_example['request']['body']}"
        request_tokens = tokenizer(request_text, truncation=True, padding="max_length", max_length=512,
                                   return_tensors="pt")

        # Обработка блока Control Flow
        control_flow_text = "\n".join([f"{k}: {v}" for k, v in json_example['control_flow'].items()])
        control_flow_tokens = tokenizer(control_flow_text, truncation=True, padding="max_length", max_length=512,
                                        return_tensors="pt")

        # Обработка блока Response
        response_text = f"Status Code: {json_example['response']['status_code']}\n" \
                        f"Headers: {json_example['response']['headers']}"
        response_tokens = tokenizer(response_text, truncation=True, padding="max_length", max_length=512,
                                    return_tensors="pt")

        return {
            "request_input_ids": request_tokens["input_ids"].squeeze(0).to(device),
            "request_attention_mask": request_tokens["attention_mask"].squeeze(0).to(device),
            "control_flow_input_ids": control_flow_tokens["input_ids"].squeeze(0).to(device),
            "control_flow_attention_mask": control_flow_tokens["attention_mask"].squeeze(0).to(device),
            "response_input_ids": response_tokens["input_ids"].squeeze(0).to(device),
            "response_attention_mask": response_tokens["attention_mask"].squeeze(0).to(device),
        }

    def run(self, context_id: int, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Команда для запуска плагина.
        :param context_id: Идентификатор контекста.
        :param data: Данные контекста, преобразованные в словарь.
        :return: Список уязвимостей.
        """
        try:
            vulnerabilities = []
            context_processed = self.preprocess_context(data)

            logger.info("Запуск ML-модели для анализа контекста %s", str(context_id))

            logits = model(
                request_input=context_processed["request_input_ids"].unsqueeze(0).to(device),
                request_mask=context_processed["request_attention_mask"].unsqueeze(0).to(device),
                control_flow_input=context_processed["control_flow_input_ids"].unsqueeze(0).to(device),
                control_flow_mask=context_processed["control_flow_attention_mask"].unsqueeze(0).to(device),
                response_input=context_processed["response_input_ids"].unsqueeze(0).to(device),
                response_mask=context_processed["response_attention_mask"].unsqueeze(0).to(device)
            )
            logger.info(logits)
            predicted_class = torch.argmax(logits, dim=1).item()
            logger.info("Завершена ML-обработка для анализа контекста %s", str(context_id))
            logger.warning(id2label[predicted_class])

            # dangerous_commands = ["ping", "ls", "cat", "wget", "curl", "rm", "bash", "sh"]
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
