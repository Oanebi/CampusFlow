
def find_ticket(tickets, ticket_id):
    """Find a ticket by its ID."""

    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            return ticket

    raise ValueError(f"Ticket '{ticket_id}' was not found.")


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign a ticket to a staff member."""

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name cannot be empty.")

    ticket = find_ticket(tickets, ticket_id)

    if ticket.get("status") == "resolved":
        raise ValueError(
            "Resolved tickets must be reopened before they can be modified."
        )

    ticket["assigned_to"] = staff_name.strip()
    return ticket


def update_ticket_status(tickets, ticket_id, new_status):
    """Update ticket status while enforcing workflow rules."""

    allowed_statuses = ("open", "in_progress", "resolved")

    if not isinstance(new_status, str) or new_status not in allowed_statuses:
        raise ValueError("Status must be open, in_progress, or resolved.")

    ticket = find_ticket(tickets, ticket_id)
    current_status = ticket.get("status")

    if current_status == "resolved":
        if new_status != "open":
            raise ValueError(
                "Resolved tickets must be reopened before changing status."
            )

    elif current_status == "open":
        if new_status == "in_progress":
            if not ticket.get("assigned_to"):
                raise ValueError(
                    "A ticket must be assigned before moving to in_progress."
                )
        elif new_status != "open":
            raise ValueError("An open ticket must move to in_progress first.")

    elif current_status == "in_progress":
        if new_status not in ("in_progress", "resolved"):
            raise ValueError(
                "An in-progress ticket can only remain in progress "
                "or be resolved."
            )

    else:
        raise ValueError("The ticket has an invalid current status.")

    ticket["status"] = new_status
    return ticket


def get_work_queue(tickets):
    """Return unresolved tickets sorted by priority and numeric ticket ID."""

    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    unresolved_tickets = [
        ticket
        for ticket in tickets
        if ticket.get("status") != "resolved"
    ]

    return sorted(
        unresolved_tickets,
        key=lambda ticket: (
            priority_order.get(ticket.get("priority"), 4),
            int(ticket["id"][1:]),
        ),
    )


def list_tickets(tickets):
    """Return all tickets as a list."""

    return list(tickets)


def view_ticket(tickets, ticket_id):
    """Return the details of a ticket by ID."""

    return find_ticket(tickets, ticket_id)
