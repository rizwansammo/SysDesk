from datetime import timedelta

from django.utils import timezone

from .models import SLA


class SLAService:
    @staticmethod
    def get_policy_for_ticket(ticket):
        return SLA.objects.filter(
            organization=ticket.organization,
            priority=ticket.priority,
            is_active=True,
        ).first()

    @staticmethod
    def get_first_response_deadline(ticket):
        policy = SLAService.get_policy_for_ticket(ticket)
        if not policy:
            return None
        return ticket.created_at + timedelta(minutes=policy.first_response_minutes)

    @staticmethod
    def get_resolution_deadline(ticket):
        policy = SLAService.get_policy_for_ticket(ticket)
        if not policy:
            return None
        return ticket.created_at + timedelta(minutes=policy.resolution_minutes)

    @staticmethod
    def is_first_response_breached(ticket):
        if ticket.first_response_at:
            deadline = SLAService.get_first_response_deadline(ticket)
            return bool(deadline and ticket.first_response_at > deadline)

        deadline = SLAService.get_first_response_deadline(ticket)
        return bool(deadline and timezone.now() > deadline)

    @staticmethod
    def is_resolution_breached(ticket):
        if ticket.resolved_at:
            deadline = SLAService.get_resolution_deadline(ticket)
            return bool(deadline and ticket.resolved_at > deadline)

        deadline = SLAService.get_resolution_deadline(ticket)
        return bool(deadline and timezone.now() > deadline)

    @staticmethod
    def get_ticket_sla_summary(ticket):
        policy = SLAService.get_policy_for_ticket(ticket)
        first_response_deadline = SLAService.get_first_response_deadline(ticket)
        resolution_deadline = SLAService.get_resolution_deadline(ticket)

        return {
            "policy_id": policy.id if policy else None,
            "policy_name": policy.name if policy else None,
            "priority": ticket.priority,
            "first_response_deadline": first_response_deadline,
            "resolution_deadline": resolution_deadline,
            "first_response_breached": SLAService.is_first_response_breached(ticket) if policy else False,
            "resolution_breached": SLAService.is_resolution_breached(ticket) if policy else False,
        }