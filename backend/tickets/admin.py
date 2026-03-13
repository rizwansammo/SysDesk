from django.contrib import admin

from .models import Ticket, TicketReply, TicketAttachment, TicketHistory


class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 0


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 0


class TicketHistoryInline(admin.TabularInline):
    model = TicketHistory
    extra = 0
    readonly_fields = ("event_type", "field_name", "old_value", "new_value", "message", "actor", "created_at")
    can_delete = False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_number",
        "subject",
        "organization",
        "created_by",
        "assigned_agent",
        "status",
        "priority",
        "source",
        "created_at",
    )
    list_filter = ("status", "priority", "source", "organization")
    search_fields = ("ticket_number", "subject", "description")
    readonly_fields = ("ticket_number", "first_response_at", "resolved_at", "closed_at", "created_at", "updated_at")
    inlines = [TicketReplyInline, TicketAttachmentInline, TicketHistoryInline]


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "author", "is_internal", "created_at")
    list_filter = ("is_internal", "created_at")
    search_fields = ("ticket__ticket_number", "ticket__subject", "body")


@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "original_name", "uploaded_by", "size", "created_at")
    search_fields = ("ticket__ticket_number", "original_name")


@admin.register(TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "event_type", "actor", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("ticket__ticket_number", "message")