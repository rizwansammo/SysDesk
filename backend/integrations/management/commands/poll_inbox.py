from django.core.management.base import BaseCommand

from integrations.tasks import poll_support_inbox


class Command(BaseCommand):
    help = "Poll the support inbox and process unread emails."

    def handle(self, *args, **options):
        results = poll_support_inbox()

        if not results:
            self.stdout.write(self.style.WARNING("No unread emails found."))
            return

        for item in results:
            if item["status"] == "processed":
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Processed email from {item['from_email']} | subject: {item['subject']} | result: {item['result']}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"Failed email from {item['from_email']} | subject: {item['subject']} | error: {item['error']}"
                    )
                )