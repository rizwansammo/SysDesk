from django.core.management.base import BaseCommand

from accounts.models import Role
from core.constants import (
    ROLE_SUPER_ADMIN,
    ROLE_AGENT,
    ROLE_END_USER,
    ROLE_VIP_USER,
)


class Command(BaseCommand):
    help = "Seed default system roles"

    def handle(self, *args, **options):
        roles = [
            (ROLE_SUPER_ADMIN, "Super Admin"),
            (ROLE_AGENT, "Agent"),
            (ROLE_END_USER, "End User"),
            (ROLE_VIP_USER, "VIP User"),
        ]

        for code, name in roles:
            Role.objects.get_or_create(code=code, defaults={"name": name})

        self.stdout.write(self.style.SUCCESS("Roles seeded successfully"))