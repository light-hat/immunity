from django.db import models


class IastProjectVersion(models.Model):
    version_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    current_version = models.PositiveSmallIntegerField(default=0)
    status = models.PositiveSmallIntegerField()
    create_time = models.IntegerField(_("create time"), default=get_timestamp)
    update_time = models.IntegerField(_("update time"), default=get_timestamp)
    user = models.ForeignKey(User, models.DO_NOTHING)
    project = models.ForeignKey(IastProject, models.DO_NOTHING)

    class Meta:
        db_table = "iast_project_version"
