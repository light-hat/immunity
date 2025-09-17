from core.models.agent import IastAgent
from core.models.project import IastProject
from django.db import models


class IastThirdPartyService(models.Model):
    agent = models.ForeignKey(
        IastAgent,
        on_delete=models.CASCADE,
        db_constraint=False,
        db_index=True,
        db_column="agent_id",
    )
    project = models.ForeignKey(
        IastProject, models.DO_NOTHING, blank=True, default=-1, db_constraint=False
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    service_type = models.CharField(max_length=255, blank=True, null=True)
    port = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "iast_third_party_service"
