"""
Плагин для детектирования CWE-77.
"""

import re
from typing import Any, Dict, List

from engine.plugins.base import BasePlugin


class CommandInjectionPlugin(BasePlugin):
    """
    Плагин для обнаружения CWE-77 (Command Injection).
    Проверяет наличие признаков выполнения команд в HTTP-запросах.
    """

    name = "command_injection_plugin"
    description = "Detects potential command injection vulnerabilities."

    def run(self, context_id: int, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        vulnerabilities = []
        request = data.get("request", {})
        url = request.get("url", "")
        body = request.get("body", "")
        headers = request.get("headers", {})

        # Правила для детекта выполнения команд

        # --- Правило 4: Подозрительные команды в теле запроса ---
        dangerous_commands = ["ping", "ls", "cat", "wget", "curl", "rm", "bash", "sh"]
        if any(cmd in body for cmd in dangerous_commands):
            vulnerabilities.append(
                {
                    # "context_id": context_id,
                    "type": "Command Injection",
                    "cwe": "CWE-77",
                    "description": f"Command '{cmd}' found in request body.",
                    "evidence": body,
                }
            )

        # --- Правило 8: Тело содержит bash команды ---
        if re.search(r"bash\s+-c\s+['\"]?.*['\"]?", body):
            vulnerabilities.append(
                {
                    # "context_id": context_id,
                    "type": "Command Injection",
                    "cwe": "CWE-77",
                    "description": "Bash command execution detected in request body.",
                    "evidence": body,
                }
            )

        # --- Правило 9: Признаки вызова системных команд через `exec` ---
        if re.search(r"exec\((['\"].*['\"])\)", body):
            vulnerabilities.append(
                {
                    # "context_id": context_id,
                    "type": "Command Injection",
                    "cwe": "CWE-77",
                    "description": "Potential system command execution using 'exec'.",
                    "evidence": body,
                }
            )

        # --- Правило 10: Прямые вызовы команд через eval ---
        if re.search(r"eval\((['\"].*(bash|sh|cmd).*)\)", body):
            vulnerabilities.append(
                {
                    # "context_id": context_id,
                    "type": "Command Injection",
                    "cwe": "CWE-77",
                    "description": "Command execution detected using 'eval'.",
                    "evidence": body,
                }
            )

        vulnerabilities.append(
            {
                # "context_id": context_id,
                "type": "Command Injection",
                "cwe": "CWE-77",
                "description": "Just test",
                "evidence": body,
            }
        )

        return vulnerabilities
