from rest_framework import serializers


class StatusCountSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()


class OrganizationCountSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField()
    organization_name = serializers.CharField()
    count = serializers.IntegerField()


class PriorityCountSerializer(serializers.Serializer):
    priority = serializers.CharField()
    count = serializers.IntegerField()


class AgentWorkloadSerializer(serializers.Serializer):
    agent_id = serializers.IntegerField()
    agent_name = serializers.CharField()
    agent_email = serializers.CharField()
    open_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()
    resolved_count = serializers.IntegerField()
    closed_count = serializers.IntegerField()
    total_count = serializers.IntegerField()


class MetricSerializer(serializers.Serializer):
    value = serializers.FloatField(allow_null=True)


class DashboardSerializer(serializers.Serializer):
    tickets_by_status = StatusCountSerializer(many=True)
    tickets_by_organization = OrganizationCountSerializer(many=True)
    tickets_by_priority = PriorityCountSerializer(many=True)
    agent_workload = AgentWorkloadSerializer(many=True)
    avg_first_response_minutes = serializers.FloatField(allow_null=True)
    avg_resolution_minutes = serializers.FloatField(allow_null=True)
    sla_breached_count = serializers.IntegerField()
    open_tickets_count = serializers.IntegerField()
    pending_tickets_count = serializers.IntegerField()
    resolved_tickets_count = serializers.IntegerField()
    closed_tickets_count = serializers.IntegerField()