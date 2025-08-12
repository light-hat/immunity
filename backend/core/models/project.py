import os.path
import string
import time

from django.db import models
#from shortuuid.django_fields import ShortUUIDField

from core.models.user_profile import UserProfile
# from core.models.strategy_user import IastStrategyUser
# from config.settings import DOMAIN_VUL


class VulValidation(models.IntegerChoices):
    FOLLOW_GLOBAL = 0
    ENABLE = 1
    DISABLE = 2
    __empty__ = 0


class ProjectStatus(models.IntegerChoices):
    NORMAL = 0, "normal"
    ERROR = 1, "error"
    OFFLINE = 2, "offline"
    __empty__ = 0


class IastProjectTemplate(models.Model):
    template_name = models.CharField(max_length=255)
    latest_time = models.IntegerField(default=int(time.time()))
    user = models.ForeignKey(UserProfile, models.DO_NOTHING)
    # scan = models.ForeignKey(IastStrategyUser, models.DO_NOTHING)
    vul_validation = models.IntegerField(default=0, choices=VulValidation.choices)
    is_system = models.IntegerField(default=0)
    data_gather = models.JSONField(default=dict)
    data_gather_is_followglobal = models.IntegerField(default=1)
    blacklist_is_followglobal = models.IntegerField(default=1)

    class Meta:
        db_table = "iast_project_template"

    def to_full_template(self):
        pass

    def to_full_project_args(self):
        return {
            "scan_id": self.scan_id,  # type: ignore
            "vul_validation": self.vul_validation,
            "data_gather": self.data_gather,
            "data_gather_is_followglobal": self.data_gather_is_followglobal,
            "blacklist_is_followglobal": self.blacklist_is_followglobal,
        }


class IastProject(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    mode = models.CharField(default="Instrumentation mode", max_length=255, blank=True)
    vul_count = models.PositiveIntegerField(blank=True, null=True)
    agent_count = models.IntegerField(blank=True, null=True)
    latest_time = models.IntegerField(default=int(time.time()))
    user = models.ForeignKey(UserProfile, models.DO_NOTHING)
    # scan = models.ForeignKey(IastStrategyUser, models.DO_NOTHING, blank=True, null=True)

    vul_validation = models.IntegerField(default=0, choices=VulValidation.choices)
    base_url = models.CharField(max_length=255, blank=True)
    test_req_header_key = models.CharField(max_length=511, blank=True)
    test_req_header_value = models.CharField(max_length=511, blank=True)
    data_gather = models.JSONField(null=True)
    data_gather_is_followglobal = models.IntegerField(default=1)
    blacklist_is_followglobal = models.IntegerField(default=1)
    template = models.ForeignKey(IastProjectTemplate, models.DO_NOTHING)
    enable_log = models.BooleanField(null=True)
    log_level = models.CharField(max_length=511, null=True, blank=True)
    last_has_online_agent_time = models.IntegerField(default=int(time.time()))
    status = models.IntegerField(default=0, choices=ProjectStatus.choices)
    #projectgroups = models.ManyToManyField("IastProjectGroup", through="IastProjectGroupProject")
    #users = models.ManyToManyField("User", through="IastProjectUser", related_name="auth_projects")
    #token = ShortUUIDField(max_length=22, alphabet=string.ascii_letters + string.digits)

    class Meta:
        db_table = "iast_project"

    def update_latest(self):
        self.latest_time = int(time.time())
        self.save(update_fields=["latest_time"])

    # def get_url(self):
    #     return os.path.join(DOMAIN_VUL, "project/projectDetail", str(self.id))
