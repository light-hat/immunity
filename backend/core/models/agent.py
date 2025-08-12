import time

from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models.project_version import IastProjectVersion
from core.models.project import IastProject
from core.models.server import IastServer


def get_events():
    return ["Registration successful"]


class IastAgent(models.Model):
    """
    IAST agent - application instrumentation module for interactive security analysis.
    """

    token = models.CharField(max_length=255, blank=True)
    version = models.CharField(max_length=255, blank=True)
    latest_time = models.IntegerField()
    server = models.ForeignKey(
        to=IastServer,
        on_delete=models.DO_NOTHING,
        related_name="agents",
        related_query_name="agent",
        verbose_name=_("server"),
    )
    is_audit = models.IntegerField()
    is_running = models.IntegerField()
    is_core_running = models.IntegerField()
    control = models.IntegerField()
    is_control = models.IntegerField()
    bind_project = models.ForeignKey(IastProject, on_delete=models.CASCADE, default=-1)
    project_version = models.ForeignKey(
        IastProjectVersion, on_delete=models.CASCADE, default=-1
    )
    project_name = models.CharField(max_length=255, blank=True)
    online = models.PositiveSmallIntegerField(default=0)
    language = models.CharField(max_length=10, blank=True)
    filepathsimhash = models.CharField(max_length=255, blank=True)
    servicetype = models.CharField(max_length=255, blank=True)
    alias = models.CharField(max_length=255, blank=True)
    startup_time = models.IntegerField(default=0)
    register_time = models.IntegerField(default=0)
    actual_running_status = models.IntegerField(default=1)
    except_running_status = models.IntegerField(default=1)
    state_status = models.IntegerField(default=1)
    events = models.JSONField(default=get_events)
    allow_report = models.IntegerField(default=1)

    class Meta:
        db_table = "iast_agent"

    def append_events(self, event: str):
        self.update_events_if_need()
        events_list = self.events if self.events else ["Registration successful"]
        events_list.append(event)
        self.events = events_list
        self.save()
        IastAgentEvent.objects.create(agent_id=self.id, name=event)

    def only_register(self):
        events_list = self.events if self.events else ["Registration successful"]
        return events_list == ["Registration successful"]

    def update_events(self):
        for event in self.events:
            IastAgentEvent.objects.create(agent_id=self.id, name=event, time=None)

    def is_need_to_update(self):
        if self.events and len(self.events) <= self.new_events.count():
            return False
        return True

    def update_events_if_need(self):
        if self.is_need_to_update():
            self.update_events()


class IastAgentEvent(models.Model):
    """
    Events that occur during agent operation.
    """

    agent = models.ForeignKey(
        IastAgent, on_delete=models.CASCADE, related_name="new_events"
    )
    name = models.CharField(max_length=255, blank=True)
    time = models.IntegerField(default=int(time.time()), blank=True, null=True)

    class Meta:
        db_table = "iast_agent_event"
