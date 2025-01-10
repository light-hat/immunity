"""
Модуль для асинхронной обработки контекста выполнения запросов.
"""

import logging
import pip_audit
from datetime import datetime
import subprocess
import json
import tempfile
from celery import shared_task
from django.db import transaction
import engine.engine as en
from core.models import Context, Event, Project, Request, Response, Configuration, Library, DependencyVulnerability
from engine.handler import ContextHandler

from engine.config_audit import ConfigAuditor, DjangoConfigAudit, FlaskConfigAudit

logger = logging.getLogger(__name__)


def _handle_request(project, context, json_request):
    """
    Создание объекта запроса в базе данных.
    :param project: объект анализируемого проекта.
    :param context: объект контекста выполнения запроса.
    :param json_request: данные о запросе в формате json.
    :return: None.
    """
    try:
        Request.objects.create(
            project=project,
            context=context,
            method=json_request["method"],
            path=json_request["path"],
            body=json_request["body"],
            headers=json_request["headers"],
            user=json_request["user"] if "user" in json_request else "Anonymous",
            get_params=json_request["GET"] if "GET" in json_request else "",
            post_params=json_request["POST"] if "POST" in json_request else "",
            cookies=json_request["COOKIES"] if "COOKIES" in json_request else "",
            files=json_request["FILES"] if "FILES" in json_request else "",
            meta=json_request["META"] if "META" in json_request else "",
        )
    except Exception as e:
        logger.error("Ошибка обработки перехваченного запроса: %s", e, exc_info=True)
        raise


def _handle_control_flow(project, context, json_control_flow):
    """
    Обработка потока управления.
    Создание объектов событий в базе данных.
    :param project: объект анализируемого проекта.
    :param context: объект контекста выполнения запроса.
    :param json_control_flow: данные о контексте выполнения запроса в формате json.
    :return: None.
    """
    try:
        for node in json_control_flow:
            if node["event"] == "external_call" or node["event"] == "internal_call":
                Event.objects.create(
                    project=project,
                    context=context,
                    timestamp=datetime.strptime(node["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    external_call=(node["event"] == "external_call"),
                    type="function_call",
                    func_name=node["name"],
                    module=node["module"],
                    filename=node["filename"],
                    line=node["line"],
                    args=node["args"],
                )
            elif node["event"] == "code_line":
                Event.objects.create(
                    project=project,
                    context=context,
                    timestamp=datetime.strptime(node["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    type="code_execution",
                    func_name=node["name"],
                    module=node["module"],
                    filename=node["filename"],
                    line=node["line"],
                    args=node["args"],
                    code=node["code"],
                )
            elif node["event"] == "return":
                Event.objects.create(
                    project=project,
                    context=context,
                    timestamp=datetime.strptime(node["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    type="return_function",
                    func_name=node["name"],
                    module=node["module"],
                    filename=node["filename"],
                    line=node["line"],
                    # final_state=node["final_state"],
                    # returned_value=node["returned_value"] if "returned_value" in node else "None",
                )
            elif node["event"] == "error":
                Event.objects.create(
                    project=project,
                    context=context,
                    timestamp=datetime.strptime(node["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    type="error",
                    func_name=node["source"][0]["function"],
                    module=node["source"][0]["module"],
                    filename=node["source"][0]["filename"],
                    line=node["source"][0]["line"],
                    exception_type=node["details"]["exception_type"],
                    exception_message=node["details"]["message"],
                )
    except Exception as e:
        logger.error("Ошибка обработки события потока управления: %s", e, exc_info=True)
        raise


def _handle_response(project, context, json_response):
    """
    Создание объекта ответа в базе данных.
    :param project: объект анализируемого проекта.
    :param context: объект контекста выполнения запроса.
    :param json_response: данные о контексте выполнения запроса в формате json.
    :return: None.
    """
    try:
        Response.objects.create(
            project=project,
            context=context,
            status_code=json_response["status"],
            headers=json_response["headers"],
            body=json_response["body"],
            content_type=(
                json_response["content_type"] if "content_type" in json_response else ""
            ),
            content_length=(
                json_response["content_length"]
                if "content_length" in json_response
                else ""
            ),
            charset=json_response["charset"] if "charset" in json_response else "",
            version=json_response["version"] if "version" in json_response else "",
            reason_phrase=(
                json_response["reason_phrase"]
                if "reason_phrase" in json_response
                else ""
            ),
            cookies=json_response["cookies"] if "cookies" in json_response else "",
            streaming=(
                json_response["streaming"] if "streaming" in json_response else ""
            ),
        )
    except Exception as e:
        logger.error("Ошибка обработки перехваченного ответа: %s", e, exc_info=True)
        raise


@shared_task
def handle_context(project_id, json_request, json_control_flow, json_response):
    """
    Асинхронный таск для отправки загруженного файла на
    анализ и вызова формирования отчёта.
    """

    try:

        logger.info("Обработка контекста проекта %s", project_id)

        with transaction.atomic():
            try:
                app = Project.objects.get(name=project_id)

                context = Context.objects.create(
                    project=app,
                )

                _handle_request(app, context, json_request)
                _handle_control_flow(app, context, json_control_flow)
                _handle_response(app, context, json_response)

            except Exception as e:
                logger.error(e)

        en.run_analysis_task.delay(app.id, context.id, ContextHandler.handle(context))

        logger.info(
            "Завершена обработка контекста %s проекта %s", context.id, project_id
        )

    except Exception as e:
        logger.error(e)


@shared_task
def handle_config(project_id, json_dict, framework_name):
    """
    Асинхронный таск для обработки, сохранения и анализа конфигурации.
    """

    try:

        logger.info("Обработка конфигурации проекта %s", project_id)

        with transaction.atomic():
            try:
                app = Project.objects.get(name=project_id)

                try:
                    old_config = Configuration.objects.filter(project=app)
                    old_config.delete()
                except ObjectDoesNotExist:
                    pass

                for setting_key, setting_value in json_dict.items():

                    Configuration.objects.create(
                        project=app,
                        key=setting_key,
                        value=setting_value
                    )

                issues = []

                if framework_name == "django":
                    django_auditor = ConfigAuditor(DjangoConfigAudit(json_dict))
                    issues = django_auditor.audit()
                elif framework_name == "flask":
                    flask_auditor = ConfigAuditor(FlaskConfigAudit(json_dict))
                    issues = flask_auditor.audit()

                for issue in issues:
                    try:
                        configuration = Configuration.objects.get(key=issue["key"])
                        configuration.vulnerable = True
                        configuration.message = issue["message"]
                        configuration.save()
                    except Exception as e:
                        logger.error(e)
                        continue

            except Exception as e:
                logger.error(e)

        logger.info(
            "Завершена обработка конфигурации проекта %s", project_id
        )

    except Exception as e:
        logger.error(e)

def _run_pip_audit(packages):
    """
    Выполняет pip-audit с временным файлом requirements.txt.

    :param packages: Словарь с именем и версией пакета, например: {"requests": "2.28.1"}
    :return: Список найденных уязвимостей
    """
    try:
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".txt", delete=False) as temp_file:
            # Формируем содержимое requirements.txt
            for name, version in packages.items():
                temp_file.write(f"{name}=={version}\n")
            temp_file.flush()  # Убедимся, что данные записаны

            # Запускаем pip-audit по временному файлу
            command = [
                "pip-audit",
                "-r", temp_file.name,
                "-f", "json",
                "--progress-spinner", "off"
            ]
            result = subprocess.run(command, capture_output=True, text=True, check=False)

            # Читаем и парсим вывод JSON
            audit_results = json.loads(result.stdout)
            return audit_results
    except subprocess.CalledProcessError as e:
        logger.info(f"Ошибка выполнения команды pip-audit: {e.stderr}")
        return []
    except Exception as ex:
        logger.info(f"Произошла ошибка: {ex}")
        return []
    finally:
        # Удаляем временный файл
        if 'temp_file' in locals():
            temp_file.close()

@shared_task
def handle_dependencies(project_id, json_dict):
    """
    Асинхронный таск для обработки, сохранения и анализа зависимостей.
    """

    try:

        logger.info("Обработка зависимостей проекта %s", project_id)

        with transaction.atomic():
            try:
                app = Project.objects.get(name=project_id)

                try:
                    Library.objects.filter(project=app).delete()
                except ObjectDoesNotExist:
                    pass

                findings = _run_pip_audit(json_dict)
                # Перебираем каждую зависимость
                for dependency in findings['dependencies']:

                    lib = Library.objects.create(
                        project=app,
                        key=dependency['name'],
                        value=dependency['version'],
                    )

                    # Проверяем, есть ли уязвимости
                    if dependency['vulns']:
                        lib.vulnerable = True
                        lib.save()
                        for vuln in dependency['vulns']:
                            DependencyVulnerability.objects.create(
                                dependency=lib,
                                label=vuln['id'],
                                recommended_version=', '.join(vuln['fix_versions']),
                            )
                    else:
                        lib.vulnerable = False
                        lib.save()

            except Exception as e:
                logger.error(e)

        logger.info(
            "Завершена обработка зависимостей проекта %s", project_id
        )

    except Exception as e:
        logger.error(e)
