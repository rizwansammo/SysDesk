from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsSupportStaff
from .models import Organization
from .serializers import OrganizationCreateUpdateSerializer, OrganizationSerializer


class OrganizationListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get(self, request):
        queryset = Organization.objects.all().order_by("name")
        serializer = OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role.code != "super_admin":
            return Response(
                {"detail": "Only super admins can create organizations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = OrganizationCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = Organization.objects.create(
            name=serializer.validated_data["name"],
            domain=serializer.validated_data["domain"],
            email=serializer.validated_data.get("email", ""),
            phone=serializer.validated_data.get("phone", ""),
            address=serializer.validated_data.get("address", ""),
            is_active=serializer.validated_data.get("is_active", True),
        )

        return Response(
            OrganizationSerializer(organization).data,
            status=status.HTTP_201_CREATED,
        )


class OrganizationRetrieveUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get_object(self, pk):
        return get_object_or_404(Organization, pk=pk)

    def get(self, request, pk):
        organization = self.get_object(pk)
        return Response(OrganizationSerializer(organization).data)

    def patch(self, request, pk):
        if request.user.role.code != "super_admin":
            return Response(
                {"detail": "Only super admins can update organizations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        organization = self.get_object(pk)

        serializer = OrganizationCreateUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        if "name" in data:
            organization.name = data["name"]
        if "domain" in data:
            organization.domain = data["domain"]
        if "email" in data:
            organization.email = data["email"]
        if "phone" in data:
            organization.phone = data["phone"]
        if "address" in data:
            organization.address = data["address"]
        if "is_active" in data:
            organization.is_active = data["is_active"]

        organization.save()

        return Response(OrganizationSerializer(organization).data)