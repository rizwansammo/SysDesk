from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from .models import Ticket
from .permissions import CanAccessTicket, IsSupportStaff
from .serializers import (
    AddReplySerializer,
    AssignTicketSerializer,
    ChangePrioritySerializer,
    ChangeStatusSerializer,
    CreateTicketSerializer,
    MergeTicketSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
)
from .services import TicketService


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related(
        "organization",
        "created_by",
        "assigned_agent",
    ).prefetch_related(
        "replies",
        "attachments",
        "history",
    )
    permission_classes = [IsAuthenticated, CanAccessTicket]
    filterset_fields = ["status", "priority", "organization", "assigned_agent", "source"]
    search_fields = ["ticket_number", "subject", "description"]
    ordering_fields = ["created_at", "updated_at", "priority"]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if user.role.code in ["super_admin", "agent"]:
            return queryset

        return queryset.filter(
            organization=user.organization,
            created_by=user,
        )

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "retrieve":
            return TicketDetailSerializer
        return TicketDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket = TicketService.create_ticket(
            actor=request.user,
            organization=request.user.organization,
            subject=serializer.validated_data["subject"],
            description=serializer.validated_data["description"],
            category=serializer.validated_data.get("category", ""),
            priority=serializer.validated_data.get("priority", Ticket.PRIORITY_MEDIUM),
            source=Ticket.SOURCE_PORTAL,
        )

        return Response(
            TicketDetailSerializer(ticket, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def reply(self, request, pk=None):
        ticket = self.get_object()

        serializer = AddReplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data["is_internal"] and request.user.role.code not in ["super_admin", "agent"]:
            return Response(
                {"detail": "Only agents can add internal notes."},
                status=status.HTTP_403_FORBIDDEN,
            )

        reply = TicketService.add_reply(
            ticket=ticket,
            actor=request.user,
            body=serializer.validated_data["body"],
            is_internal=serializer.validated_data["is_internal"],
        )

        return Response(
            {
                "message": "Reply added successfully",
                "reply_id": reply.id,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsSupportStaff])
    def assign(self, request, pk=None):
        ticket = self.get_object()

        serializer = AssignTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assigned_agent = None
        assigned_agent_id = serializer.validated_data.get("assigned_agent_id")

        if assigned_agent_id:
            assigned_agent = get_object_or_404(
                User,
                id=assigned_agent_id,
                role__code__in=["agent", "super_admin"],
            )

        TicketService.assign_ticket(
            ticket=ticket,
            actor=request.user,
            assigned_agent=assigned_agent,
        )

        return Response({"message": "Ticket assignment updated successfully"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsSupportStaff])
    def change_status(self, request, pk=None):
        ticket = self.get_object()

        serializer = ChangeStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        TicketService.change_status(
            ticket=ticket,
            actor=request.user,
            new_status=serializer.validated_data["status"],
        )

        return Response({"message": "Ticket status updated successfully"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsSupportStaff])
    def change_priority(self, request, pk=None):
        ticket = self.get_object()

        serializer = ChangePrioritySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        TicketService.change_priority(
            ticket=ticket,
            actor=request.user,
            new_priority=serializer.validated_data["priority"],
        )

        return Response({"message": "Ticket priority updated successfully"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def reopen(self, request, pk=None):
        ticket = self.get_object()

        if request.user.role.code not in ["super_admin", "agent"] and ticket.created_by_id != request.user.id:
            return Response({"detail": "You cannot reopen this ticket."}, status=status.HTTP_403_FORBIDDEN)

        TicketService.reopen_ticket(
            ticket=ticket,
            actor=request.user,
        )

        return Response({"message": "Ticket reopened successfully"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsSupportStaff])
    def merge(self, request, pk=None):
        source_ticket = self.get_object()

        serializer = MergeTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_ticket = get_object_or_404(Ticket, id=serializer.validated_data["target_ticket_id"])

        if source_ticket.id == target_ticket.id:
            return Response(
                {"detail": "A ticket cannot be merged into itself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        TicketService.merge_tickets(
            source_ticket=source_ticket,
            target_ticket=target_ticket,
            actor=request.user,
        )

        return Response({"message": "Ticket merged successfully"})