from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsSupportStaff
from .serializers import DashboardSerializer
from .services import ReportService


class DashboardReportView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get(self, request):
        data = ReportService.dashboard_summary()
        serializer = DashboardSerializer(data)
        return Response(serializer.data)


class TicketsByStatusReportView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get(self, request):
        return Response(ReportService.tickets_by_status())


class TicketsByOrganizationReportView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get(self, request):
        return Response(ReportService.tickets_by_organization())


class TicketsByPriorityReportView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get(self, request):
        return Response(ReportService.tickets_by_priority())


class AgentWorkloadReportView(APIView):
    permission_classes = [IsAuthenticated, IsSupportStaff]

    def get(self, request):
        return Response(ReportService.agent_workload())