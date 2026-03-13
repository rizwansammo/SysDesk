from rest_framework import serializers

from organizations.models import Organization
from .models import SLA


class SLASerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = SLA
        fields = [
            "id",
            "name",
            "organization",
            "organization_name",
            "priority",
            "first_response_minutes",
            "resolution_minutes",
            "is_active",
            "created_at",
            "updated_at",
        ]


class SLACreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    organization = serializers.IntegerField(required=False)
    priority = serializers.ChoiceField(choices=SLA.PRIORITY_CHOICES, required=False)
    first_response_minutes = serializers.IntegerField(required=False, min_value=1)
    resolution_minutes = serializers.IntegerField(required=False, min_value=1)
    is_active = serializers.BooleanField(required=False)

    def validate_organization(self, value):
        if not Organization.objects.filter(id=value).exists():
            raise serializers.ValidationError("Selected organization does not exist.")
        return value