from django.conf import settings
from django.db import models

from core.mixins import TimeStampedModel
from organizations.models import Organization


class AuditLog(TimeStampedModel):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    entity_type = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=64)
    action = models.CharField(max_length=100)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["entity_type", "entity_id"]),
            models.Index(fields=["action"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.entity_type} #{self.entity_id} - {self.action}"