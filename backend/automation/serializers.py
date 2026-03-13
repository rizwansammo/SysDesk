from rest_framework import serializers

from organizations.models import Organization
from .models import AutomationRule


class AutomationRuleSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = AutomationRule
        fields = [
            "id",
            "name",
            "organization",
            "organization_name",
            "is_active",
            "trigger_event",
            "conditions",
            "actions",
            "priority",
            "created_at",
            "updated_at",
        ]


class AutomationRuleCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    organization = serializers.IntegerField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)
    trigger_event = serializers.ChoiceField(
        choices=AutomationRule.TRIGGER_CHOICES,
        required=False,
    )
    conditions = serializers.JSONField(required=False)
    actions = serializers.JSONField(required=False)
    priority = serializers.IntegerField(required=False, min_value=1)

    def validate_organization(self, value):
        if value is None:
            return value
        if not Organization.objects.filter(id=value).exists():
            raise serializers.ValidationError("Selected organization does not exist.")
        return value