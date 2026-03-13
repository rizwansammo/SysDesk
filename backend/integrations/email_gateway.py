from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Role
from core.constants import ROLE_END_USER
from organizations.models import Organization
from tickets.models import Ticket
from tickets.services import TicketService

from .parsers import extract_ticket_number, normalize_email_address

User = get_user_model()


class EmailGatewayError(Exception):
    pass


class EmailGateway:
    @classmethod
    @transaction.atomic
    def process_incoming_email(
        cls,
        *,
        from_email: str,
        subject: str,
        body: str,
    ):
        normalized_email = normalize_email_address(from_email)

        if not normalized_email:
            raise EmailGatewayError("Sender email is required.")

        ticket_number = extract_ticket_number(subject)

        sender_user = (
            User.objects.select_related("organization", "role")
            .filter(email__iexact=normalized_email, is_active=True)
            .first()
        )

        if ticket_number:
            existing_ticket = (
                Ticket.objects.select_related("organization", "created_by", "assigned_agent")
                .filter(ticket_number=ticket_number)
                .first()
            )

            if existing_ticket:
                if not sender_user:
                    sender_user = cls._get_or_create_user_from_ticket_context(
                        email=normalized_email,
                        ticket=existing_ticket,
                    )

                reply = TicketService.add_reply(
                    ticket=existing_ticket,
                    actor=sender_user,
                    body=body,
                    is_internal=False,
                )
                return {
                    "type": "reply",
                    "ticket_id": existing_ticket.id,
                    "ticket_number": existing_ticket.ticket_number,
                    "reply_id": reply.id,
                }

        organization = cls._resolve_organization_for_sender(normalized_email)

        if not organization:
            raise EmailGatewayError(
                f"No organization could be resolved for sender: {normalized_email}"
            )

        if not sender_user:
            sender_user = cls._create_end_user_for_email(
                email=normalized_email,
                organization=organization,
            )

        ticket = TicketService.create_ticket(
            actor=sender_user,
            organization=organization,
            subject=subject or "(No Subject)",
            description=body or "",
            category="",
            priority=Ticket.PRIORITY_MEDIUM,
            source=Ticket.SOURCE_EMAIL,
        )

        return {
            "type": "ticket",
            "ticket_id": ticket.id,
            "ticket_number": ticket.ticket_number,
        }

    @staticmethod
    def _resolve_organization_for_sender(email: str):
        domain = email.split("@")[-1].lower()
        return Organization.objects.filter(domain__iexact=domain, is_active=True).first()

    @staticmethod
    def _get_or_create_user_from_ticket_context(email: str, ticket):
        existing_user = (
            User.objects.select_related("organization", "role")
            .filter(email__iexact=email, is_active=True)
            .first()
        )
        if existing_user:
            return existing_user

        return EmailGateway._create_end_user_for_email(
            email=email,
            organization=ticket.organization,
        )

    @staticmethod
    def _create_end_user_for_email(email: str, organization):
        role = Role.objects.filter(code=ROLE_END_USER).first()
        if not role:
            raise EmailGatewayError("End User role does not exist. Run seed_roles first.")

        local_part = email.split("@")[0]
        first_name = local_part[:150]

        return User.objects.create_user(
            email=email,
            password=None,
            first_name=first_name,
            last_name="",
            organization=organization,
            role=role,
            is_active=True,
        )