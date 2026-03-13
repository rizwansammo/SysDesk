from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsSupportStaff
from organizations.models import Organization
from .models import SLA
from .serializers import SLACreateUpdateSerializer, SLASerializer


class SLAListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get(self, request):
        queryset = SLA.objects.select_related("organization").all().order_by("organization__name", "priority")
        serializer = SLASerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role.code != "super_admin":
            return Response(
                {"detail": "Only super admins can create SLA policies."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = SLACreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = get_object_or_404(Organization, id=serializer.validated_data["organization"])

        sla = SLA.objects.create(
            name=serializer.validated_data["name"],
            organization=organization,
            priority=serializer.validated_data["priority"],
            first_response_minutes=serializer.validated_data["first_response_minutes"],
            resolution_minutes=serializer.validated_data["resolution_minutes"],
            is_active=serializer.validated_data.get("is_active", True),
        )

        return Response(SLASerializer(sla).data, status=status.HTTP_201_CREATED)


class SLARetrieveUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get_object(self, pk):
        return get_object_or_404(SLA.objects.select_related("organization"), pk=pk)

    def get(self, request, pk):
        sla = self.get_object(pk)
        return Response(SLASerializer(sla).data)

    def patch(self, request, pk):
        if request.user.role.code != "super_admin":
            return Response(
                {"detail": "Only super admins can update SLA policies."},
                status=status.HTTP_403_FORBIDDEN,
            )

        sla = self.get_object(pk)

        serializer = SLACreateUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if "name" in data:
            sla.name = data["name"]
        if "organization" in data:
            sla.organization = get_object_or_404(Organization, id=data["organization"])
        if "priority" in data:
            sla.priority = data["priority"]
        if "first_response_minutes" in data:
            sla.first_response_minutes = data["first_response_minutes"]
        if "resolution_minutes" in data:
            sla.resolution_minutes = data["resolution_minutes"]
        if "is_active" in data:
            sla.is_active = data["is_active"]

        sla.save()

        return Response(SLASerializer(sla).data)