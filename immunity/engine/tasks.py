import os
import time
from datetime import datetime
from os import environ
from pathlib import Path

from celery import shared_task
from django.conf import settings
from user_api.models import *


@shared_task
def handle_context(project_id, json_request, json_control_flow, json_response):
    """
    Асинхронный таск для отправки загруженного файла на
    анализ и вызова формирования отчёта.
    """

    app = Application.objects.get(name=project_id)

    context = Context.objects.create(
        application=app,
    )

    try:

        Request.objects.create(
            context=context,
            method=json_request["method"],
            path=json_request["path"],
            body=json_request["body"],
            headers=json_request["headers"],
            user=json_request["user"],
            get_params=json_request["GET"],
            post_params=json_request["POST"],
            cookies=json_request["COOKIES"],
            files=json_request["FILES"],
            meta=json_request["META"],
        )

        control_flow = ControlFlow.objects.create(context=context)

        try:

            for node in json_control_flow:
                if node["event"] == "external_call" or node["event"] == "internal_call":
                    FunctionCall.objects.create(
                        control_flow=control_flow,
                        timestamp=datetime.strptime(
                            node["timestamp"], "%Y-%m-%d %H:%M:%S"
                        ),
                        external_call=(
                            True if node["event"] == "external_call" else False
                        ),
                        name=node["name"],
                        module=node["module"],
                        filename=node["filename"],
                        line=node["line"],
                        args=node["args"],
                    )
                elif node["event"] == "code_line":
                    CodeExecution.objects.create(
                        control_flow=control_flow,
                        timestamp=datetime.strptime(
                            node["timestamp"], "%Y-%m-%d %H:%M:%S"
                        ),
                        func_name=node["name"],
                        module=node["module"],
                        filename=node["filename"],
                        line=node["line"],
                        args=node["args"],
                        code=node["code"],
                    )
                elif node["event"] == "return":
                    ReturnFunction.objects.create(
                        control_flow=control_flow,
                        timestamp=datetime.strptime(
                            node["timestamp"], "%Y-%m-%d %H:%M:%S"
                        ),
                        func_name=node["name"],
                        module=node["module"],
                        filename=node["filename"],
                        line=node["line"],
                        final_state=node["final_state"],
                        returned_value=node["returned_value"],
                    )
                elif node["event"] == "error":
                    Error.objects.create(
                        control_flow=control_flow,
                        timestamp=datetime.strptime(
                            node["timestamp"], "%Y-%m-%d %H:%M:%S"
                        ),
                        source_function=node["source"][0]["function"],
                        source_module=node["source"][0]["module"],
                        source_filename=node["source"][0]["filename"],
                        source_line=node["source"][0]["line"],
                        exception_type=node["details"]["exception_type"],
                        exception_message=node["details"]["message"],
                    )

        except Exception as e:
            print(f"Handle control flow ERROR: {str(e)}")
            pass

        Response.objects.create(
            context=context,
            status_code=json_response["status"],
            headers=json_response["headers"],
            body=json_response["body"],
            content_type=json_response["content_type"],
            content_length=(
                json_response["content_length"]
                if json_response["content_length"]
                else ""
            ),
            charset=json_response["charset"] if json_response["charset"] else "",
            version=json_response["version"] if json_response["version"] else "",
            reason_phrase=json_response["reason_phrase"],
            cookies=json_response["cookies"],
            streaming=json_response["streaming"],
        )

    except Exception as e:
        print(f"Handle context ERROR: {str(e)}")
