from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from organizations.models import Organization
from .models import Role, User
from .permissions import IsSuperAdmin, IsSupportStaff
from .serializers import (
    UserCreateSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserDetailSerializer(request.user).data)


class UserListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get(self, request):
        queryset = User.objects.select_related("organization", "role").all()

        if request.user.role.code == "agent":
            queryset = queryset.exclude(role__code="super_admin")

        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role.code != "super_admin":
            return Response(
                {"detail": "Only super admins can create users."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        role = get_object_or_404(Role, id=serializer.validated_data["role"])
        organization = None

        organization_id = serializer.validated_data.get("organization")
        if organization_id is not None:
            organization = get_object_or_404(Organization, id=organization_id)

        user = User.objects.create_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data.get("last_name", ""),
            organization=organization,
            role=role,
            phone=serializer.validated_data.get("phone", ""),
            job_title=serializer.validated_data.get("job_title", ""),
            is_active=serializer.validated_data.get("is_active", True),
        )

        return Response(
            UserDetailSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class UserRetrieveUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get_object(self, pk, request):
        queryset = User.objects.select_related("organization", "role").all()

        if request.user.role.code == "agent":
            queryset = queryset.exclude(role__code="super_admin")

        return get_object_or_404(queryset, pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk, request)
        return Response(UserDetailSerializer(user).data)

    def patch(self, request, pk):
        if request.user.role.code != "super_admin":
            return Response(
                {"detail": "Only super admins can update users."},
                status=status.HTTP_403_FORBIDDEN,
            )

        user = self.get_object(pk, request)

        serializer = UserUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "phone" in data:
            user.phone = data["phone"]
        if "job_title" in data:
            user.job_title = data["job_title"]
        if "is_active" in data:
            user.is_active = data["is_active"]
        if "role" in data:
            user.role = get_object_or_404(Role, id=data["role"])
        if "organization" in data:
            if data["organization"] is None:
                user.organization = None
            else:
                user.organization = get_object_or_404(Organization, id=data["organization"])

        user.save()

        return Response(UserDetailSerializer(user).data)


class AgentListView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get(self, request):
        queryset = User.objects.select_related("organization", "role").filter(
            role__code__in=["agent", "super_admin"],
            is_active=True,
        )
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)