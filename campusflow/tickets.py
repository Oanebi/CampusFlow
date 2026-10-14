def calculate_priority(urgency, affected_users):
    """Calculate a ticket's priority from urgency and affected users."""

    if not isinstance(urgency, str):
        raise ValueError("Urgency must be low, medium, or high.")

    urgency = urgency.lower().strip()

    if urgency not in ("low", "medium", "high"):
        raise ValueError("Urgency must be low, medium, or high.")

    if (
        not isinstance(affected_users, int)
        or isinstance(affected_users, bool)
        or affected_users < 1
    ):
        raise ValueError("Affected users must be a positive integer.")

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


def generate_ticket_id(existing_tickets):
    """Generate the next available ticket ID."""

    existing_ids = {
        ticket["id"]
        for ticket in existing_tickets
        if isinstance(ticket, dict) and isinstance(ticket.get("id"), str)
    }

    number = 1

    while f"T{number:03d}" in existing_ids:
        number += 1

    return f"T{number:03d}"



def create_ticket(title, category, urgency, affected_users, existing_tickets=None):
    """Create and return a validated campus helpdesk ticket."""

    # Check that the title is a string and is not empty.
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title must be a non-empty string.")

    # Reject titles containing only digits, such as "0001" or "999".
    if title.strip().isdigit():
        raise ValueError("Ticket title must describe a campus problem.")

    # Validate the category.
    if not isinstance(category, str) or not category.strip():
        raise ValueError("Ticket category cannot be empty.")

    if existing_tickets is None:
        existing_tickets = []

    if not isinstance(existing_tickets, list):
        raise ValueError("Existing tickets must be provided as a list.")

    ticket_id = generate_ticket_id(existing_tickets)
    priority = calculate_priority(urgency, affected_users)

    return {
        "id": ticket_id,
        "title": title.strip(),
        "category": category.strip(),
        "urgency": urgency.strip().lower(),
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }
