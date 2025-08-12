"""
Module for defining Django models.
"""

from core.models.agent_thirdservice import *
from core.models.agent import *
# from core.models.api_route import *
from core.models.heartbeat import *
# from core.models.hook_strategy import *
# from core.models.hook_type import *
# from core.models.method_pool import *
from core.models.program_language import *
from core.models.project_version import *
from core.models.project import *
from core.models.server import *
# from core.models.strategy import *
from core.models.user_profile import *
from core.models.vul_level import *
# from core.models.vulnerability import *

LANGUAGE_DICT = {"JAVA": 1, "PYTHON": 2, "PHP": 3, "GO": 4}

LANGUAGE_ID_DICT = {"1": "JAVA", "2": "PYTHON", "3": "PHP", "4": "GO"}

AVAILABILITY_DICT = {
    "1": "Exploit code exists",
    "2": "Analysis article exists",
    "3": "No utilization information",
}

SOURCE_TYPE_DICT = {
    "1": "Application vulnerabilities",
    "2": "Component vulnerabilities",
}

AGGREGATION_ORDER = {
    "1": "vul.level_id",
    "2": "vul.create_time",
    "3": "vul.update_time",
}

APP_VUL_ORDER = {
    "1": "level_id",
    "2": "first_time",
    "3": "latest_time",
    "4": "status_id",
}
# license risk level
LICENSE_RISK = {
    "1": "high",
    "2": "middle",
    "3": "Low",
    "0": "no risk",
    "4": "no risk",
}
LICENSE_RISK_DESC = {
    "1": "Commercial closed-source integration is prohibited",
    "2": "Restrictive commercial closed-source integration",
    "3": "Partial commercial closed-source integration",
    "0": "No commercial closed-source integration",
    "4": "No commercial closed-source integration",
}
# Vulnerability level
APP_LEVEL_RISK = {
    "1": "high risk",
    "2": "medium risk",
    "3": "low risk",
    "4": "no risk",
    "5": "hint",
    "0": "no risk",
}

# Component vulnerability exploitability
SCA_AVAILABILITY_DICT = {
    "1": "Exploit code exists",
    "2": "Analysis article exists",
    "3": "No utilization information",
}

VUL_TYPE_CSS = {
    "1": "sca-height",
    "2": "sca-middle",
    "3": "sca-low",
    "4": "sca-info",
}

VUL_DEP_CSS = {
    "1": "height",
    "2": "middle",
    "3": "low",
    "4": "info",
}

DEFAULT_EXPORT_REPORT_DICT = {
    "description": {
        "user_id": "user_id",
        "report_name": "report_name",
        "project_name": "",
        "version_name": "version_name",
        "api_vount": "",
        "vul_level_count": {},
        "license_level_count": {},
        "project_create_time": "",
        "report_create_time": "",
    },
    "risk_analysis": {
        "content": "",
        "level_png": "",
        "trend_png": "",
        "app_vul_type": {
            "1": {},
            "2": {},
            "3": {},
            "4": {},
            "5": {},
        },
        "sca_vul_type": {
            "1": {},
            "2": {},
            "3": {},
            "4": {},
            "5": {},
        },
        "license_type": {},
    },
    "risk_details": {
        "app_vul_detail": [],
        "sca_vul_detail": [],
        "license_vul_detail": [],
    },
    "sca_list": {},
    "api_site_map": {},
}
