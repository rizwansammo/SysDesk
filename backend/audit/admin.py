from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "entity_type",
        "entity_id",
        "action",
        "actor",
        "organization",
        "created_at",
    )
    list_filter = ("entity_type", "action", "organization", "created_at")
    search_fields = ("entity_type", "entity_id", "action", "actor__email")
    readonly_fields = (
        "organization",
        "actor",
        "entity_type",
        "entity_id",
        "action",
        "metadata",
        "ip_address",
        "user_agent",
        "created_at",
        "updated_at",
    )