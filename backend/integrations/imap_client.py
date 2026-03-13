import email
import imaplib
from email.header import decode_header

from django.conf import settings


class IMAPClientError(Exception):
    pass


class IMAPClient:
    def __init__(self):
        self.host = settings.IMAP_HOST
        self.port = settings.IMAP_PORT
        self.username = settings.IMAP_USERNAME
        self.password = settings.IMAP_PASSWORD
        self.connection = None

    def connect(self):
        if not self.host or not self.username or not self.password:
            raise IMAPClientError("IMAP settings are not configured properly.")

        self.connection = imaplib.IMAP4_SSL(self.host, self.port)
        self.connection.login(self.username, self.password)
        self.connection.select("INBOX")
        return self.connection

    def close(self):
        if self.connection:
            try:
                self.connection.close()
            except Exception:
                pass
            try:
                self.connection.logout()
            except Exception:
                pass

    def fetch_unread_messages(self):
        if not self.connection:
            self.connect()

        status, message_numbers = self.connection.search(None, "UNSEEN")
        if status != "OK":
            raise IMAPClientError("Failed to search unread emails.")

        messages = []
        for num in message_numbers[0].split():
            status, msg_data = self.connection.fetch(num, "(RFC822)")
            if status != "OK":
                continue

            raw_email = msg_data[0][1]
            message = email.message_from_bytes(raw_email)

            parsed = self._parse_message(message)
            parsed["imap_num"] = num
            messages.append(parsed)

        return messages

    def mark_as_seen(self, imap_num):
        if self.connection and imap_num:
            self.connection.store(imap_num, "+FLAGS", "\\Seen")

    def _parse_message(self, message):
        subject = self._decode_header_value(message.get("Subject", ""))
        from_email = email.utils.parseaddr(message.get("From", ""))[1]
        body = self._extract_body(message)

        return {
            "subject": subject,
            "from_email": from_email,
            "body": body,
            "message_id": message.get("Message-ID", ""),
            "in_reply_to": message.get("In-Reply-To", ""),
        }

    def _decode_header_value(self, value):
        decoded_parts = decode_header(value)
        parts = []

        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                parts.append(part.decode(encoding or "utf-8", errors="ignore"))
            else:
                parts.append(part)

        return "".join(parts)

    def _extract_body(self, message):
        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                if "attachment" in content_disposition.lower():
                    continue

                if content_type == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode(part.get_content_charset() or "utf-8", errors="ignore").strip()

            for part in message.walk():
                if part.get_content_type() == "text/html":
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode(part.get_content_charset() or "utf-8", errors="ignore").strip()

            return ""
        else:
            payload = message.get_payload(decode=True)
            if payload:
                return payload.decode(message.get_content_charset() or "utf-8", errors="ignore").strip()
            return ""