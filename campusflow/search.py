"""Read-only ticket search and filtering."""

PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}

VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}
VALID_CATEGORIES = {"network", "hardware", "software", "other"}


def search_tickets(
    tickets,
    title="",
    category=None,
    status=None,
    priority=None,
):
    """Return tickets matching every supplied filter."""

    if not isinstance(tickets, list):
        raise ValueError("Tickets must be provided as a list.")

    if not isinstance(title, str):
        raise ValueError("Search title must be a string.")

    # Ignore case, spaces, and punctuation when searching titles.
    title_query = "".join(
        character
        for character in title.casefold()
        if character.isalnum()
    )

    if category is not None:
        if not isinstance(category, str):
            raise ValueError("Category must be a string.")

        category = category.strip().casefold()

        if category not in VALID_CATEGORIES:
            raise ValueError("Invalid category.")

    if status is not None:
        if not isinstance(status, str):
            raise ValueError("Status must be a string.")

        status = status.strip().casefold()

        if status not in VALID_STATUSES:
            raise ValueError("Invalid status.")

    if priority is not None:
        if not isinstance(priority, str):
            raise ValueError("Priority must be a string.")

        priority = priority.strip().casefold()

        if priority not in VALID_PRIORITIES:
            raise ValueError("Invalid priority.")

    results = []

    for ticket in tickets:
        if not isinstance(ticket, dict):
            continue

        ticket_title = ticket.get("title", "")

        if not isinstance(ticket_title, str):
            ticket_title = ""

        normalized_title = "".join(
            character
            for character in ticket_title.casefold()
            if character.isalnum()
        )

        if title_query and title_query not in normalized_title:
            continue

        if category is not None:
            ticket_category = ticket.get("category", "")

            if not isinstance(ticket_category, str):
                continue

            if ticket_category.strip().casefold() != category:
                continue

        if status is not None:
            ticket_status = ticket.get("status", "")

            if not isinstance(ticket_status, str):
                continue

            if ticket_status.strip().casefold() != status:
                continue

        if priority is not None:
            ticket_priority = ticket.get("priority", "")

            if not isinstance(ticket_priority, str):
                continue

            if ticket_priority.strip().casefold() != priority:
                continue

        results.append(ticket)

    return results


def sort_search_results_by_priority(tickets):
    """Return a sorted copy without modifying the original list."""

    def sort_key(ticket):
        priority = ticket.get("priority", "")

        if not isinstance(priority, str):
            priority = ""

        ticket_id = ticket.get("id", "")

        if not isinstance(ticket_id, str):
            ticket_id = ""

        digits = "".join(
            character
            for character in ticket_id
            if character.isdigit()
        )

        numeric_id = int(digits) if digits else float("inf")

        return (
            PRIORITY_ORDER.get(priority.casefold(), 99),
            numeric_id,
            ticket_id,
        )

    return sorted(tickets, key=sort_key)
