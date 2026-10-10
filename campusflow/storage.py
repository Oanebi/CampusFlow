
import json
from pathlib import Path


def save_tickets(tickets, filename="data/tickets.json"):
    """Save tickets to a JSON file."""

    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def load_tickets(filename="data/tickets.json"):
    """Load tickets from a JSON file."""

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

    if not isinstance(tickets, list):
        raise ValueError(
            f"Ticket data in '{filename}' must contain a JSON list."
        )

    return tickets
