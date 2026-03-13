from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsSupportStaff
from organizations.models import Organization
from .models import AutomationRule
from .serializers import AutomationRuleCreateUpdateSerializer, AutomationRuleSerializer


class AutomationRuleListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get(self, request):
        queryset = AutomationRule.objects.select_related("organization").all().order_by("priority", "id")
        serializer = AutomationRuleSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role.code != "super_admin":
            return Response(
                {"detail": "Only super admins can create automation rules."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AutomationRuleCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = None
        organization_id = serializer.validated_data.get("organization")
        if organization_id is not None:
            organization = get_object_or_404(Organization, id=organization_id)

        rule = AutomationRule.objects.create(
            name=serializer.validated_data["name"],
            organization=organization,
            is_active=serializer.validated_data.get("is_active", True),
            trigger_event=serializer.validated_data["trigger_event"],
            conditions=serializer.validated_data.get("conditions", {}),
            actions=serializer.validated_data.get("actions", {}),
            priority=serializer.validated_data.get("priority", 100),
        )

        return Response(AutomationRuleSerializer(rule).data, status=status.HTTP_201_CREATED)


class AutomationRuleRetrieveUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get_object(self, pk):
        return get_object_or_404(AutomationRule.objects.select_related("organization"), pk=pk)

    def get(self, request, pk):
        rule = self.get_object(pk)
        return Response(AutomationRuleSerializer(rule).data)

    def patch(self, request, pk):
        if request.user.role.code != "super_admin":
            return Response(
                {"detail": "Only super admins can update automation rules."},
                status=status.HTTP_403_FORBIDDEN,
            )

        rule = self.get_object(pk)

        serializer = AutomationRuleCreateUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if "name" in data:
            rule.name = data["name"]
        if "organization" in data:
            if data["organization"] is None:
                rule.organization = None
            else:
                rule.organization = get_object_or_404(Organization, id=data["organization"])
        if "is_active" in data:
            rule.is_active = data["is_active"]
        if "trigger_event" in data:
            rule.trigger_event = data["trigger_event"]
        if "conditions" in data:
            rule.conditions = data["conditions"]
        if "actions" in data:
            rule.actions = data["actions"]
        if "priority" in data:
            rule.priority = data["priority"]

        rule.save()

        return Response(AutomationRuleSerializer(rule).data)