from integrations.smtp_client import SMTPNotificationService


class TicketNotificationService:
    @staticmethod
    def send_ticket_created(ticket):
        recipient = ticket.created_by.email
        subject = f"[{ticket.ticket_number}] Ticket received: {ticket.subject}"
        message = (
            f"Hello {ticket.created_by.full_name or ticket.created_by.email},\n\n"
            f"Your ticket has been received in SysDesk.\n\n"
            f"Ticket Number: {ticket.ticket_number}\n"
            f"Subject: {ticket.subject}\n"
            f"Status: {ticket.status}\n"
            f"Priority: {ticket.priority}\n\n"
            f"We will get back to you soon.\n\n"
            f"SysDesk Helpdesk"
        )

        return SMTPNotificationService.send_email(
            subject=subject,
            message=message,
            recipient_list=[recipient],
        )

    @staticmethod
    def send_public_reply(ticket, reply):
        recipient = ticket.created_by.email
        subject = f"Re: [{ticket.ticket_number}] {ticket.subject}"
        message = (
            f"Hello {ticket.created_by.full_name or ticket.created_by.email},\n\n"
            f"There is a new reply on your ticket.\n\n"
            f"Ticket Number: {ticket.ticket_number}\n"
            f"Reply From: {reply.author.full_name or reply.author.email}\n\n"
            f"Reply:\n{reply.body}\n\n"
            f"Current Status: {ticket.status}\n"
            f"Current Priority: {ticket.priority}\n\n"
            f"SysDesk Helpdesk"
        )

        return SMTPNotificationService.send_email(
            subject=subject,
            message=message,
            recipient_list=[recipient],
        )

    @staticmethod
    def send_status_changed(ticket, old_status, new_status):
        recipient = ticket.created_by.email
        subject = f"[{ticket.ticket_number}] Status updated: {new_status}"
        message = (
            f"Hello {ticket.created_by.full_name or ticket.created_by.email},\n\n"
            f"Your ticket status has been updated.\n\n"
            f"Ticket Number: {ticket.ticket_number}\n"
            f"Subject: {ticket.subject}\n"
            f"Previous Status: {old_status}\n"
            f"New Status: {new_status}\n\n"
            f"SysDesk Helpdesk"
        )

        return SMTPNotificationService.send_email(
            subject=subject,
            message=message,
            recipient_list=[recipient],
        )