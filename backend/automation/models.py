from django.db import models

from core.mixins import TimeStampedModel
from organizations.models import Organization


class AutomationRule(TimeStampedModel):
    TRIGGER_TICKET_CREATED = "ticket_created"
    TRIGGER_TICKET_UPDATED = "ticket_updated"

    TRIGGER_CHOICES = [
        (TRIGGER_TICKET_CREATED, "Ticket Created"),
        (TRIGGER_TICKET_UPDATED, "Ticket Updated"),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="automation_rules",
    )
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    trigger_event = models.CharField(max_length=50, choices=TRIGGER_CHOICES)
    conditions = models.JSONField(default=dict, blank=True)
    actions = models.JSONField(default=dict, blank=True)
    priority = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["priority", "id"]

    def __str__(self):
        return self.name