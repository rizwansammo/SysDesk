from django.db import models

from core.mixins import TimeStampedModel
from organizations.models import Organization


class SLA(TimeStampedModel):
    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_CRITICAL = "critical"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
        (PRIORITY_CRITICAL, "Critical"),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="sla_policies",
    )
    name = models.CharField(max_length=255)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    first_response_minutes = models.PositiveIntegerField()
    resolution_minutes = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["organization__name", "priority"]
        unique_together = [("organization", "priority")]

    def __str__(self):
        return f"{self.organization.name} - {self.priority}"