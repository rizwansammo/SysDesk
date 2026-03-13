from celery import shared_task

from integrations.email_gateway import EmailGateway, EmailGatewayError
from integrations.imap_client import IMAPClient


@shared_task
def poll_support_inbox():
    client = IMAPClient()

    try:
        client.connect()
        messages = client.fetch_unread_messages()
        results = []

        for message in messages:
            try:
                result = EmailGateway.process_incoming_email(
                    from_email=message["from_email"],
                    subject=message["subject"],
                    body=message["body"],
                )
                client.mark_as_seen(message["imap_num"])

                results.append({
                    "status": "processed",
                    "from_email": message["from_email"],
                    "subject": message["subject"],
                    "result": result,
                })
            except EmailGatewayError as exc:
                results.append({
                    "status": "failed",
                    "from_email": message["from_email"],
                    "subject": message["subject"],
                    "error": str(exc),
                })

        return results

    finally:
        client.close()