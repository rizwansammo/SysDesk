import re


TICKET_NUMBER_PATTERN = re.compile(r"\b(SD-\d{17})\b", re.IGNORECASE)


def extract_ticket_number(subject: str) -> str | None:
    if not subject:
        return None

    match = TICKET_NUMBER_PATTERN.search(subject)
    if not match:
        return None

    return match.group(1).upper()


def normalize_email_address(email: str) -> str:
    return (email or "").strip().lower()