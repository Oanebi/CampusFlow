"""Read-only ticket search and filtering."""

PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}

VALID_CATEGORIES = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}

VALID_STATUSES = {
    "open",
    "in_progress",
    "resolved",
}

VALID_PRIORITIES = {
    "critical",
    "high",
    "medium",
    "low",
}


def search_tickets(
    tickets,
    title="",
    category=None,
    status=None,
    priority=None,
):
    """Return tickets matching every supplied search condition.

    Search is read-only: it returns a new list and does not edit tickets.
    Title matching uses case-insensitive substring matching.
    """

    if not isinstance(title, str):
        raise ValueError("Search title must be a string.")

    if category is not None:
        if not isinstance(category, str):
            raise ValueError("Category must be a string.")

        category = VALID_CATEGORIES.get(category.strip().casefold())

        if category is None:
            raise ValueError(
                "Category must be Network, Hardware, Software, or Other."
            )

    if status is not None:
        if not isinstance(status, str):
            raise ValueError("Status must be a string.")

        status = status.strip().casefold()

        if status not in VALID_STATUSES:
            raise ValueError(
                "Status must be open, in_progress, or resolved."
            )

    if priority is not None:
        if not isinstance(priority, str):
            raise ValueError("Priority must be a string.")

        priority = priority.strip().casefold()

        if priority not in VALID_PRIORITIES:
            raise ValueError(
                "Priority must be critical, high, medium, or low."
            )

    title_query = "".join(
    character for character in title.casefold()
    if character.isalnum()
)
    results = []

    for ticket in tickets:
        if not isinstance(ticket, dict):
            continue

        ticket_title = ticket.get("title", "")

        if not isinstance(ticket_title, str):
            continue

        # Every supplied condition must match.
        normalized_ticket_title = "".join(
    character for character in ticket_title.casefold()
    if character.isalnum()
)

if title_query and title_query not in normalized_ticket_title:
    continue

        if category is not None:
            if ticket.get("category") != category:
                continue

        if status is not None:
            if ticket.get("status") != status:
                continue

        if priority is not None:
            if ticket.get("priority") != priority:
                continue

        results.append(ticket)

    return results


def sort_search_results_by_priority(tickets):
    """Return a new list ordered by priority, then numeric ticket ID."""

    def sort_key(ticket):
        priority = ticket.get("priority")

        if not isinstance(priority, str):
            priority = ""

        ticket_id = ticket.get("id", "")

        # Extract the numeric portion of IDs such as T001 and T010.
        number = (
            int(ticket_id[1:])
            if (
                isinstance(ticket_id, str)
                and len(ticket_id) > 1
                and ticket_id[0].casefold() == "t"
                and ticket_id[1:].isdigit()
            )
            else float("inf")
        )

        return (
            PRIORITY_ORDER.get(priority.casefold(), len(PRIORITY_ORDER)),
            number,
            str(ticket_id),
        )

    return sorted(tickets, key=sort_key)