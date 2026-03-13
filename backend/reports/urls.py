from django.urls import path

from .views import (
    AgentWorkloadReportView,
    DashboardReportView,
    TicketsByOrganizationReportView,
    TicketsByPriorityReportView,
    TicketsByStatusReportView,
)

urlpatterns = [
    path("dashboard/", DashboardReportView.as_view(), name="reports-dashboard"),
    path("tickets-by-status/", TicketsByStatusReportView.as_view(), name="reports-tickets-by-status"),
    path("tickets-by-organization/", TicketsByOrganizationReportView.as_view(), name="reports-tickets-by-organization"),
    path("tickets-by-priority/", TicketsByPriorityReportView.as_view(), name="reports-tickets-by-priority"),
    path("agent-workload/", AgentWorkloadReportView.as_view(), name="reports-agent-workload"),
]