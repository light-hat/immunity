from django.db import models

from core.models.hook_strategy import HookStrategy


class MethodPool(models.Model):
    """
    Method Pool - is what an agent creates when processing a request.
    """

    id = models.BigAutoField(primary_key=True)
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, db_constraint=False)
    url = models.CharField(max_length=2000, blank=True)
    uri = models.CharField(max_length=2000, blank=True)
    http_method = models.CharField(max_length=10, blank=True)
    http_scheme = models.CharField(max_length=20, blank=True)
    http_protocol = models.CharField(max_length=255, blank=True)
    req_header = models.CharField(max_length=2000, blank=True, null=True)
    req_params = models.CharField(max_length=2000, blank=True, null=True)
    req_data = models.CharField(max_length=4000, blank=True, null=True)
    res_header = models.CharField(max_length=1000, blank=True, null=True)
    res_body = models.TextField(blank=True, null=True)
    req_header_fs = models.TextField(db_column="req_header_for_search")
    context_path = models.CharField(max_length=255, blank=True, null=True)
    method_pool = models.TextField()
    pool_sign = models.CharField(unique=True, blank=True, max_length=40)
    clent_ip = models.CharField(max_length=255, blank=True)
    create_time = models.IntegerField()
    update_time = models.IntegerField()
    uri_sha1 = models.CharField(max_length=40, blank=True, db_index=True)
    sinks = models.ManyToManyField(
        HookStrategy,
        verbose_name=_("sinks"),
        blank=True,
        related_name="method_pools",
        related_query_name="method_pool",
    )

    class Meta:
        db_table = "iast_agent_method_pool"
