from django.conf import settings
from django.core.mail import send_mail


class SMTPNotificationError(Exception):
    pass


class SMTPNotificationService:
    @staticmethod
    def send_email(*, subject, message, recipient_list):
        if not recipient_list:
            return 0

        try:
            return send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        except Exception as exc:
            raise SMTPNotificationError(str(exc)) from exc