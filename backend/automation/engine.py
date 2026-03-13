from django.contrib.auth import get_user_model

from .models import AutomationRule

User = get_user_model()


class AutomationEngine:
    @classmethod
    def run(cls, *, trigger_event, ticket, actor):
        rules = AutomationRule.objects.filter(
            is_active=True,
            trigger_event=trigger_event,
        ).order_by("priority", "id")

        for rule in rules:
            if rule.organization_id and rule.organization_id != ticket.organization_id:
                continue

            if cls._matches(rule.conditions, ticket=ticket, actor=actor):
                cls._apply(rule.actions, ticket=ticket)

    @staticmethod
    def _matches(conditions, *, ticket, actor):
        subject_contains = conditions.get("subject_contains")
        if subject_contains:
            if subject_contains.lower() not in ticket.subject.lower():
                return False

        actor_role = conditions.get("actor_role")
        if actor_role:
            if not actor.role or actor.role.code != actor_role:
                return False

        category_equals = conditions.get("category_equals")
        if category_equals:
            if (ticket.category or "").lower() != category_equals.lower():
                return False

        return True

    @staticmethod
    def _apply(actions, *, ticket):
        changed_fields = []

        set_priority = actions.get("set_priority")
        if set_priority and ticket.priority != set_priority:
            ticket.priority = set_priority
            changed_fields.append("priority")

        assign_agent_id = actions.get("assign_agent_id")
        if assign_agent_id:
            agent = User.objects.filter(
                id=assign_agent_id,
                role__code__in=["agent", "super_admin"],
                is_active=True,
            ).first()
            if agent and ticket.assigned_agent_id != agent.id:
                ticket.assigned_agent = agent
                changed_fields.append("assigned_agent")

        if changed_fields:
            changed_fields.append("updated_at")
            ticket.save(update_fields=changed_fields)