"""
Модуль для асинхронной обработки контекста выполнения запросов.
"""

import logging
from datetime import datetime

from celery import shared_task
from django.db import transaction

from core.models import Context, Event, Project, Request, Response

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

    logger.info("Обработка контекста проекта %s", project_id)

    with transaction.atomic():
        app = Project.objects.get(name=project_id)

        context = Context.objects.create(
            project=app,
        )

        _handle_request(app, context, json_request)
        _handle_control_flow(app, context, json_control_flow)
        _handle_response(app, context, json_response)

    logger.info("Завершена обработка контекста проекта %s", project_id)
