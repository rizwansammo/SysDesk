from rest_framework.permissions import BasePermission


class IsSupportStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role.code in ["super_admin", "agent"]
        )


class CanAccessTicket(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.role.code in ["super_admin", "agent"]:
            return True

        return obj.organization_id == user.organization_id and obj.created_by_id == user.id