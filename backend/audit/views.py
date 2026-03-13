from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsSupportStaff
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogListView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get(self, request):
        queryset = AuditLog.objects.select_related("organization", "actor").all()

        entity_type = request.query_params.get("entity_type")
        action = request.query_params.get("action")
        organization_id = request.query_params.get("organization")
        actor_id = request.query_params.get("actor")

        if entity_type:
            queryset = queryset.filter(entity_type=entity_type)
        if action:
            queryset = queryset.filter(action=action)
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        if actor_id:
            queryset = queryset.filter(actor_id=actor_id)

        serializer = AuditLogSerializer(queryset[:200], many=True)
        return Response(serializer.data)