from rest_framework import serializers

from organizations.models import Organization
from .models import Role, User


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "code", "name"]


class UserListSerializer(serializers.ModelSerializer):
    role_code = serializers.CharField(source="role.code", read_only=True)
    role_name = serializers.CharField(source="role.name", read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "job_title",
            "is_active",
            "organization",
            "organization_name",
            "role",
            "role_code",
            "role_name",
            "created_at",
            "updated_at",
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "job_title",
            "is_active",
            "is_staff",
            "is_superuser",
            "organization",
            "organization_name",
            "role",
            "created_at",
            "updated_at",
        ]


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, min_length=8)
    organization = serializers.IntegerField(required=False, allow_null=True)
    role = serializers.IntegerField()
    phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    job_title = serializers.CharField(max_length=120, required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False, default=True)

    def validate_role(self, value):
        if not Role.objects.filter(id=value).exists():
            raise serializers.ValidationError("Selected role does not exist.")
        return value

    def validate_organization(self, value):
        if value is None:
            return value
        if not Organization.objects.filter(id=value).exists():
            raise serializers.ValidationError("Selected organization does not exist.")
        return value


class UserUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=50, required=False, allow_blank=True)
    job_title = serializers.CharField(max_length=120, required=False, allow_blank=True)
    organization = serializers.IntegerField(required=False, allow_null=True)
    role = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)

    def validate_role(self, value):
        if not Role.objects.filter(id=value).exists():
            raise serializers.ValidationError("Selected role does not exist.")
        return value

    def validate_organization(self, value):
        if value is None:
            return value
        if not Organization.objects.filter(id=value).exists():
            raise serializers.ValidationError("Selected organization does not exist.")
        return value