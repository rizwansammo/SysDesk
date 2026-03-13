from django.contrib import admin

from .models import AutomationRule


@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "organization",
        "trigger_event",
        "priority",
        "is_active",
        "created_at",
    )
    list_filter = ("trigger_event", "is_active", "organization")
    search_fields = ("name",)