from django.conf import settings
from django.db import models
from django.utils import timezone

from core.mixins import TimeStampedModel
from organizations.models import Organization


class Ticket(TimeStampedModel):
    STATUS_OPEN = "open"
    STATUS_PENDING = "pending"
    STATUS_RESOLVED = "resolved"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_PENDING, "Pending"),
        (STATUS_RESOLVED, "Resolved"),
        (STATUS_CLOSED, "Closed"),
    ]

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

    SOURCE_PORTAL = "portal"
    SOURCE_EMAIL = "email"
    SOURCE_API = "api"

    SOURCE_CHOICES = [
        (SOURCE_PORTAL, "Portal"),
        (SOURCE_EMAIL, "Email"),
        (SOURCE_API, "API"),
    ]

    ticket_number = models.CharField(max_length=30, unique=True, db_index=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="tickets",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_tickets",
    )
    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )

    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM,
    )
    category = models.CharField(max_length=120, blank=True)
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default=SOURCE_PORTAL,
    )

    is_merged = models.BooleanField(default=False)
    merged_into = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="merged_children",
    )

    first_response_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["organization", "priority"]),
            models.Index(fields=["assigned_agent", "status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]

    def __str__(self):
        return f"{self.ticket_number} - {self.subject}"


class TicketReply(TimeStampedModel):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="replies",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="ticket_replies",
    )
    body = models.TextField()
    is_internal = models.BooleanField(default=False)

    email_message_id = models.CharField(max_length=255, blank=True)
    email_in_reply_to = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Reply #{self.id} on {self.ticket.ticket_number}"


class TicketAttachment(TimeStampedModel):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    reply = models.ForeignKey(
        TicketReply,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="attachments",
    )
    file = models.FileField(upload_to="ticket_attachments/%Y/%m/%d/")
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=120, blank=True)
    size = models.PositiveIntegerField(default=0)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="uploaded_ticket_attachments",
    )

    def __str__(self):
        return self.original_name


class TicketHistory(TimeStampedModel):
    EVENT_CREATED = "created"
    EVENT_STATUS_CHANGED = "status_changed"
    EVENT_PRIORITY_CHANGED = "priority_changed"
    EVENT_ASSIGNED = "assigned"
    EVENT_REPLY_ADDED = "reply_added"
    EVENT_INTERNAL_NOTE = "internal_note"
    EVENT_REOPENED = "reopened"
    EVENT_MERGED = "merged"

    EVENT_CHOICES = [
        (EVENT_CREATED, "Created"),
        (EVENT_STATUS_CHANGED, "Status Changed"),
        (EVENT_PRIORITY_CHANGED, "Priority Changed"),
        (EVENT_ASSIGNED, "Assigned"),
        (EVENT_REPLY_ADDED, "Reply Added"),
        (EVENT_INTERNAL_NOTE, "Internal Note"),
        (EVENT_REOPENED, "Reopened"),
        (EVENT_MERGED, "Merged"),
    ]

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="history",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ticket_history_actions",
    )
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    field_name = models.CharField(max_length=100, blank=True)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    message = models.TextField(blank=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.ticket.ticket_number} - {self.event_type}"