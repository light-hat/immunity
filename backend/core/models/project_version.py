import time

from core.models.project import IastProject
from core.models.user_profile import UserProfile
from django.db import models
from django.utils.translation import gettext_lazy as _


class IastProjectVersion(models.Model):
    version_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    current_version = models.PositiveSmallIntegerField(default=0)
    status = models.PositiveSmallIntegerField()
    create_time = models.IntegerField(_("create time"), default=int(time.time()))
    update_time = models.IntegerField(_("update time"), default=int(time.time()))
    user = models.ForeignKey(UserProfile, models.DO_NOTHING)
    project = models.ForeignKey(IastProject, models.DO_NOTHING)

    class Meta:
        db_table = "iast_project_version"
