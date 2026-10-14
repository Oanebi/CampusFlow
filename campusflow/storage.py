
import json
from pathlib import Path


def _validate_tickets(tickets, filename):
    """Validate the ticket collection before loading or saving."""

    if not isinstance(tickets, list):
        raise ValueError(
            f"Ticket data in '{filename}' must contain a JSON list."
        )

    seen_ids = set()

    for index, ticket in enumerate(tickets):
        if not isinstance(ticket, dict):
            raise ValueError(
                f"Ticket at position {index} in '{filename}' "
                "must be a JSON object."
            )

        ticket_id = ticket.get("id")

        if not isinstance(ticket_id, str) or not ticket_id.strip():
            raise ValueError(
                f"Ticket at position {index} in '{filename}' "
                "must have a non-empty string ID."
            )

        if ticket_id in seen_ids:
            raise ValueError(
                f"Duplicate ticket ID '{ticket_id}' in '{filename}'."
            )

        seen_ids.add(ticket_id)


def save_tickets(tickets, filename="data/tickets.json"):
    """Validate and save tickets to a JSON file."""

    _validate_tickets(tickets, filename)

    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def load_tickets(filename="data/tickets.json"):
    """Load and validate tickets from a JSON file."""

    path = Path(filename)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Ticket data in '{filename}' is invalid JSON."
        ) from error

    _validate_tickets(tickets, filename)

    return tickets
