import time

from core.models.hook_type import HookType
from core.models.user_profile import UserProfile
from core.models.vul_level import IastVulLevel
from django.db import models


class IastStrategyModel(models.Model):
    user = models.ForeignKey(UserProfile, models.DO_NOTHING)
    vul_type = models.CharField(max_length=255, blank=True)
    level = models.ForeignKey(IastVulLevel, models.DO_NOTHING)
    state = models.CharField(max_length=255, blank=True)
    dt = models.IntegerField(blank=True, default=int(time.time()))
    vul_name = models.CharField(max_length=255, blank=True)
    vul_desc = models.TextField()
    vul_fix = models.TextField(blank=True)
    hook_type = models.ForeignKey(HookType, models.DO_NOTHING, blank=True, null=True)
    system_type = models.IntegerField(blank=True, default=0)

    class Meta:
        db_table = "iast_strategy"
