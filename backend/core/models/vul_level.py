from django.db import models


class IastVulLevel(models.Model):
    name = models.CharField(max_length=255, blank=True)
    name_value = models.CharField(max_length=255, blank=True)
    name_type = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "iast_vul_level"
