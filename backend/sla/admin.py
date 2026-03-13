from django.contrib import admin

from .models import SLA


@admin.register(SLA)
class SLAAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "organization",
        "priority",
        "first_response_minutes",
        "resolution_minutes",
        "is_active",
        "created_at",
    )
    list_filter = ("organization", "priority", "is_active")
    search_fields = ("name", "organization__name")