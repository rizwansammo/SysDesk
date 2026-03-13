from rest_framework import serializers

from accounts.models import User
from .models import Ticket, TicketReply, TicketAttachment, TicketHistory


class TicketReplySerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    author_email = serializers.CharField(source="author.email", read_only=True)

    class Meta:
        model = TicketReply
        fields = [
            "id",
            "ticket",
            "author",
            "author_name",
            "author_email",
            "body",
            "is_internal",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "ticket",
            "author",
            "author_name",
            "author_email",
            "created_at",
            "updated_at",
        ]


class TicketAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source="uploaded_by.full_name", read_only=True)

    class Meta:
        model = TicketAttachment
        fields = [
            "id",
            "ticket",
            "reply",
            "file",
            "original_name",
            "content_type",
            "size",
            "uploaded_by",
            "uploaded_by_name",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "uploaded_by",
            "uploaded_by_name",
            "created_at",
        ]


class TicketHistorySerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source="actor.full_name", read_only=True)

    class Meta:
        model = TicketHistory
        fields = [
            "id",
            "ticket",
            "actor",
            "actor_name",
            "event_type",
            "field_name",
            "old_value",
            "new_value",
            "message",
            "created_at",
        ]
        read_only_fields = fields


class TicketListSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)
    assigned_agent_name = serializers.CharField(source="assigned_agent.full_name", read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "ticket_number",
            "subject",
            "status",
            "priority",
            "category",
            "source",
            "organization",
            "organization_name",
            "created_by",
            "created_by_name",
            "assigned_agent",
            "assigned_agent_name",
            "first_response_at",
            "resolved_at",
            "closed_at",
            "created_at",
            "updated_at",
        ]


class TicketDetailSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)
    assigned_agent_name = serializers.CharField(source="assigned_agent.full_name", read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    replies = TicketReplySerializer(many=True, read_only=True)
    attachments = TicketAttachmentSerializer(many=True, read_only=True)
    history = TicketHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "ticket_number",
            "organization",
            "organization_name",
            "created_by",
            "created_by_name",
            "assigned_agent",
            "assigned_agent_name",
            "subject",
            "description",
            "status",
            "priority",
            "category",
            "source",
            "is_merged",
            "merged_into",
            "first_response_at",
            "resolved_at",
            "closed_at",
            "created_at",
            "updated_at",
            "replies",
            "attachments",
            "history",
        ]


class CreateTicketSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    description = serializers.CharField()
    category = serializers.CharField(max_length=120, required=False, allow_blank=True)
    priority = serializers.ChoiceField(
        choices=Ticket.PRIORITY_CHOICES,
        required=False,
        default=Ticket.PRIORITY_MEDIUM,
    )


class AddReplySerializer(serializers.Serializer):
    body = serializers.CharField()
    is_internal = serializers.BooleanField(default=False)


class AssignTicketSerializer(serializers.Serializer):
    assigned_agent_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_assigned_agent_id(self, value):
        if value is None:
            return value

        if not User.objects.filter(id=value, role__code__in=["agent", "super_admin"]).exists():
            raise serializers.ValidationError("Assigned user must be an agent or super admin.")
        return value


class ChangeStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Ticket.STATUS_CHOICES)


class ChangePrioritySerializer(serializers.Serializer):
    priority = serializers.ChoiceField(choices=Ticket.PRIORITY_CHOICES)


class MergeTicketSerializer(serializers.Serializer):
    target_ticket_id = serializers.IntegerField()

    def validate_target_ticket_id(self, value):
        if not Ticket.objects.filter(id=value).exists():
            raise serializers.ValidationError("Target ticket not found.")
        return value