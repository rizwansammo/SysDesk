from .models import AuditLog


class AuditService:
    @staticmethod
    def log(
        *,
        actor=None,
        organization=None,
        entity_type,
        entity_id,
        action,
        metadata=None,
        ip_address=None,
        user_agent="",
    ):
        return AuditLog.objects.create(
            actor=actor,
            organization=organization,
            entity_type=entity_type,
            entity_id=str(entity_id),
            action=action,
            metadata=metadata or {},
            ip_address=ip_address,
            user_agent=user_agent or "",
        )