from django.db import transaction
from django.utils import timezone

from automation.engine import AutomationEngine
from .models import Ticket, TicketReply, TicketHistory


class TicketService:
    @staticmethod
    def generate_ticket_number():
        return f"SD-{timezone.now().strftime('%Y%m%d%H%M%S%f')[:-3]}"

    @classmethod
    @transaction.atomic
    def create_ticket(
        cls,
        *,
        actor,
        organization,
        subject,
        description,
        category="",
        priority=Ticket.PRIORITY_MEDIUM,
        source=Ticket.SOURCE_PORTAL,
        assigned_agent=None,
    ):
        ticket = Ticket.objects.create(
            ticket_number=cls.generate_ticket_number(),
            organization=organization,
            created_by=actor,
            assigned_agent=assigned_agent,
            subject=subject,
            description=description,
            status=Ticket.STATUS_OPEN,
            priority=priority,
            category=category,
            source=source,
        )

        AutomationEngine.run(
            trigger_event="ticket_created",
            ticket=ticket,
            actor=actor,
        )

        TicketHistory.objects.create(
            ticket=ticket,
            actor=actor,
            event_type=TicketHistory.EVENT_CREATED,
            message=f"Ticket created by {actor.email}",
        )

        return ticket

    @classmethod
    @transaction.atomic
    def add_reply(cls, *, ticket, actor, body, is_internal=False):
        reply = TicketReply.objects.create(
            ticket=ticket,
            author=actor,
            body=body,
            is_internal=is_internal,
        )

        TicketHistory.objects.create(
            ticket=ticket,
            actor=actor,
            event_type=(
                TicketHistory.EVENT_INTERNAL_NOTE
                if is_internal
                else TicketHistory.EVENT_REPLY_ADDED
            ),
            message="Internal note added" if is_internal else "Public reply added",
        )

        if not is_internal and actor.role.code in ["agent", "super_admin"] and not ticket.first_response_at:
            ticket.first_response_at = timezone.now()
            ticket.save(update_fields=["first_response_at", "updated_at"])

        return reply

    @classmethod
    @transaction.atomic
    def assign_ticket(cls, *, ticket, actor, assigned_agent):
        old_agent = ticket.assigned_agent

        ticket.assigned_agent = assigned_agent
        ticket.save(update_fields=["assigned_agent", "updated_at"])

        TicketHistory.objects.create(
            ticket=ticket,
            actor=actor,
            event_type=TicketHistory.EVENT_ASSIGNED,
            field_name="assigned_agent",
            old_value={"id": old_agent.id, "email": old_agent.email} if old_agent else None,
            new_value={"id": assigned_agent.id, "email": assigned_agent.email} if assigned_agent else None,
            message=f"Assigned to {assigned_agent.email if assigned_agent else 'Unassigned'}",
        )

        return ticket

    @classmethod
    @transaction.atomic
    def change_status(cls, *, ticket, actor, new_status):
        old_status = ticket.status
        ticket.status = new_status

        if new_status == Ticket.STATUS_RESOLVED:
            ticket.resolved_at = timezone.now()

        if new_status == Ticket.STATUS_CLOSED:
            ticket.closed_at = timezone.now()

        if new_status in [Ticket.STATUS_OPEN, Ticket.STATUS_PENDING]:
            ticket.closed_at = None

        ticket.save(update_fields=["status", "resolved_at", "closed_at", "updated_at"])

        TicketHistory.objects.create(
            ticket=ticket,
            actor=actor,
            event_type=TicketHistory.EVENT_STATUS_CHANGED,
            field_name="status",
            old_value={"status": old_status},
            new_value={"status": new_status},
            message=f"Status changed from {old_status} to {new_status}",
        )

        return ticket

    @classmethod
    @transaction.atomic
    def change_priority(cls, *, ticket, actor, new_priority):
        old_priority = ticket.priority
        ticket.priority = new_priority
        ticket.save(update_fields=["priority", "updated_at"])

        TicketHistory.objects.create(
            ticket=ticket,
            actor=actor,
            event_type=TicketHistory.EVENT_PRIORITY_CHANGED,
            field_name="priority",
            old_value={"priority": old_priority},
            new_value={"priority": new_priority},
            message=f"Priority changed from {old_priority} to {new_priority}",
        )

        return ticket

    @classmethod
    @transaction.atomic
    def reopen_ticket(cls, *, ticket, actor):
        old_status = ticket.status
        ticket.status = Ticket.STATUS_OPEN
        ticket.closed_at = None
        ticket.save(update_fields=["status", "closed_at", "updated_at"])

        TicketHistory.objects.create(
            ticket=ticket,
            actor=actor,
            event_type=TicketHistory.EVENT_REOPENED,
            field_name="status",
            old_value={"status": old_status},
            new_value={"status": Ticket.STATUS_OPEN},
            message="Ticket reopened",
        )

        return ticket

    @classmethod
    @transaction.atomic
    def merge_tickets(cls, *, source_ticket, target_ticket, actor):
        source_ticket.is_merged = True
        source_ticket.merged_into = target_ticket
        source_ticket.status = Ticket.STATUS_CLOSED
        source_ticket.closed_at = timezone.now()
        source_ticket.save(
            update_fields=["is_merged", "merged_into", "status", "closed_at", "updated_at"]
        )

        TicketHistory.objects.create(
            ticket=source_ticket,
            actor=actor,
            event_type=TicketHistory.EVENT_MERGED,
            message=f"Merged into {target_ticket.ticket_number}",
        )

        return source_ticket