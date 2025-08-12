from django.db import models


class IastProgramLanguage(models.Model):
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "iast_program_language"
