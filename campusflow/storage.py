
"""Functions for saving and loading CampusFlow tickets."""

import json
from pathlib import Path


VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES = {"low", "medium", "high"}
VALID_PRIORITIES = {"low", "medium", "high", "critical"}
VALID_STATUSES = {"open", "in_progress", "resolved"}


def _validate_tickets(tickets, filename):
    """Validate ticket records and any follow-up notes."""
    if not isinstance(tickets, list):
        raise ValueError(
            f"Ticket data in '{filename}' must contain a JSON list."
        )

    # Check ticket objects and IDs first so duplicate-ID errors
    # are not hidden by errors in other fields.
    seen_ids = set()

    for index, ticket in enumerate(tickets):
        if not isinstance(ticket, dict):
            raise ValueError(
                f"Ticket at index {index} in '{filename}' must be a JSON object."
            )

        ticket_id = ticket.get("id")

        if not isinstance(ticket_id, str) or not ticket_id.strip():
            raise ValueError(
                f"Ticket at index {index} in '{filename}' has an invalid ID."
            )

        if ticket_id in seen_ids:
            raise ValueError(
                f"Duplicate ticket ID '{ticket_id}' in '{filename}'."
            )

        seen_ids.add(ticket_id)

    # Validate fields when present. This allows older or minimal
    # ticket records to remain readable.
    for ticket in tickets:
        ticket_id = ticket["id"]

        title = ticket.get("title")
        if "title" in ticket and (
            not isinstance(title, str) or not title.strip()
        ):
            raise ValueError(
                f"Ticket '{ticket_id}' in '{filename}' has an invalid title."
            )

        category = ticket.get("category")
        if "category" in ticket and category not in VALID_CATEGORIES:
            raise ValueError(
                f"Ticket '{ticket_id}' in '{filename}' has an invalid category."
            )

        urgency = ticket.get("urgency")
        if "urgency" in ticket and urgency not in VALID_URGENCIES:
            raise ValueError(
                f"Ticket '{ticket_id}' in '{filename}' has an invalid urgency."
            )

        affected_users = ticket.get("affected_users")
        if "affected_users" in ticket and (
            not isinstance(affected_users, int)
            or isinstance(affected_users, bool)
            or affected_users < 1
        ):
            raise ValueError(
                f"Ticket '{ticket_id}' in '{filename}' has invalid affected users."
            )

        priority = ticket.get("priority")
        if "priority" in ticket and priority not in VALID_PRIORITIES:
            raise ValueError(
                f"Ticket '{ticket_id}' in '{filename}' has an invalid priority."
            )

        status = ticket.get("status")
        if "status" in ticket and status not in VALID_STATUSES:
            raise ValueError(
                f"Ticket '{ticket_id}' in '{filename}' has an invalid status."
            )

        assigned_to = ticket.get("assigned_to")
        if "assigned_to" in ticket and assigned_to is not None and (
            not isinstance(assigned_to, str) or not assigned_to.strip()
        ):
            raise ValueError(
                f"Ticket '{ticket_id}' in '{filename}' has an invalid assignee."
            )

        notes = ticket.get("notes", [])

        if not isinstance(notes, list):
            raise ValueError(
                f"Notes for ticket '{ticket_id}' in '{filename}' must be a list."
            )

        seen_note_ids = set()

        for note_index, note in enumerate(notes):
            if not isinstance(note, dict):
                raise ValueError(
                    f"Note {note_index} for ticket '{ticket_id}' "
                    f"in '{filename}' must be a JSON object."
                )

            note_id = note.get("note_id")

            if (
                not isinstance(note_id, str)
                or not note_id.startswith("N")
                or not note_id[1:].isdigit()
                or int(note_id[1:]) < 1
                or note_id != f"N{int(note_id[1:]):03d}"
            ):
                raise ValueError(
                    f"Note {note_index} for ticket '{ticket_id}' "
                    f"in '{filename}' has an invalid ID."
                )

            if note_id in seen_note_ids:
                raise ValueError(
                    f"Duplicate note ID '{note_id}' for ticket "
                    f"'{ticket_id}' in '{filename}'."
                )

            seen_note_ids.add(note_id)

            author = note.get("author")
            if not isinstance(author, str) or not author.strip():
                raise ValueError(
                    f"Note '{note_id}' for ticket '{ticket_id}' "
                    f"in '{filename}' has an invalid author."
                )

            message = note.get("message")
            if (
                not isinstance(message, str)
                or not 5 <= len(message.strip()) <= 300
            ):
                raise ValueError(
                    f"Note '{note_id}' for ticket '{ticket_id}' "
                    f"in '{filename}' has an invalid message."
                )


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
