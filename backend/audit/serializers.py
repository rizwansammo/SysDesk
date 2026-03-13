from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source="actor.full_name", read_only=True)
    actor_email = serializers.CharField(source="actor.email", read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "organization",
            "organization_name",
            "actor",
            "actor_name",
            "actor_email",
            "entity_type",
            "entity_id",
            "action",
            "metadata",
            "ip_address",
            "user_agent",
            "created_at",
            "updated_at",
        ]