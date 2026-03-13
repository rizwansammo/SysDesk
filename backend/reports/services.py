from django.db.models import Count, F

from sla.services import SLAService
from tickets.models import Ticket


class ReportService:
    @staticmethod
    def tickets_by_status():
        rows = (
            Ticket.objects.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )
        return list(rows)

    @staticmethod
    def tickets_by_priority():
        rows = (
            Ticket.objects.values("priority")
            .annotate(count=Count("id"))
            .order_by("priority")
        )
        return list(rows)

    @staticmethod
    def tickets_by_organization():
        rows = (
            Ticket.objects.values("organization_id")
            .annotate(
                organization_name=F("organization__name"),
                count=Count("id"),
            )
            .order_by("organization_name")
        )
        return list(rows)

    @staticmethod
    def agent_workload():
        rows = (
            Ticket.objects.filter(assigned_agent__isnull=False)
            .values(
                "assigned_agent_id",
                "assigned_agent__first_name",
                "assigned_agent__last_name",
                "assigned_agent__email",
                "status",
            )
            .order_by("assigned_agent_id")
        )

        summary = {}

        for row in rows:
            agent_id = row["assigned_agent_id"]

            if agent_id not in summary:
                full_name = f"{row['assigned_agent__first_name']} {row['assigned_agent__last_name']}".strip()
                summary[agent_id] = {
                    "agent_id": agent_id,
                    "agent_name": full_name,
                    "agent_email": row["assigned_agent__email"],
                    "open_count": 0,
                    "pending_count": 0,
                    "resolved_count": 0,
                    "closed_count": 0,
                    "total_count": 0,
                }

            status = row["status"]

            if status == Ticket.STATUS_OPEN:
                summary[agent_id]["open_count"] += 1
            elif status == Ticket.STATUS_PENDING:
                summary[agent_id]["pending_count"] += 1
            elif status == Ticket.STATUS_RESOLVED:
                summary[agent_id]["resolved_count"] += 1
            elif status == Ticket.STATUS_CLOSED:
                summary[agent_id]["closed_count"] += 1

            summary[agent_id]["total_count"] += 1

        return list(summary.values())

    @staticmethod
    def avg_first_response_minutes():
        tickets = Ticket.objects.filter(first_response_at__isnull=False)
        if not tickets.exists():
            return None

        total_minutes = 0.0
        count = 0

        for ticket in tickets:
            delta = ticket.first_response_at - ticket.created_at
            total_minutes += delta.total_seconds() / 60.0
            count += 1

        return round(total_minutes / count, 2) if count else None

    @staticmethod
    def avg_resolution_minutes():
        tickets = Ticket.objects.filter(resolved_at__isnull=False)
        if not tickets.exists():
            return None

        total_minutes = 0.0
        count = 0

        for ticket in tickets:
            delta = ticket.resolved_at - ticket.created_at
            total_minutes += delta.total_seconds() / 60.0
            count += 1

        return round(total_minutes / count, 2) if count else None

    @staticmethod
    def sla_breached_count():
        count = 0
        for ticket in Ticket.objects.select_related("organization").all():
            summary = SLAService.get_ticket_sla_summary(ticket)
            if summary["first_response_breached"] or summary["resolution_breached"]:
                count += 1
        return count

    @staticmethod
    def dashboard_summary():
        return {
            "tickets_by_status": ReportService.tickets_by_status(),
            "tickets_by_organization": ReportService.tickets_by_organization(),
            "tickets_by_priority": ReportService.tickets_by_priority(),
            "agent_workload": ReportService.agent_workload(),
            "avg_first_response_minutes": ReportService.avg_first_response_minutes(),
            "avg_resolution_minutes": ReportService.avg_resolution_minutes(),
            "sla_breached_count": ReportService.sla_breached_count(),
            "open_tickets_count": Ticket.objects.filter(status=Ticket.STATUS_OPEN).count(),
            "pending_tickets_count": Ticket.objects.filter(status=Ticket.STATUS_PENDING).count(),
            "resolved_tickets_count": Ticket.objects.filter(status=Ticket.STATUS_RESOLVED).count(),
            "closed_tickets_count": Ticket.objects.filter(status=Ticket.STATUS_CLOSED).count(),
        }