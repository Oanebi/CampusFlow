
import json
from pathlib import Path



def _validate_tickets(tickets, filename):
    """Validate ticket records and any follow-up notes."""

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

        # Older tickets may not have a notes field.
        notes = ticket.get("notes", [])

        if not isinstance(notes, list):
            raise ValueError(
                f"Notes for ticket '{ticket_id}' must be a list."
            )

        seen_note_ids = set()

        for note_index, note in enumerate(notes):
            if not isinstance(note, dict):
                raise ValueError(
                    f"Note at position {note_index} for ticket "
                    f"'{ticket_id}' must be a JSON object."
                )

            note_id = note.get("note_id")

            if not isinstance(note_id, str) or not note_id.startswith("N"):
                raise ValueError(
                    f"Note at position {note_index} for ticket "
                    f"'{ticket_id}' has an invalid note ID."
                )

            number_part = note_id[1:]

            if not number_part.isdigit() or int(number_part) < 1:
                raise ValueError(
                    f"Note at position {note_index} for ticket "
                    f"'{ticket_id}' has an invalid note ID."
                )

            if note_id != f"N{int(number_part):03d}":
                raise ValueError(
                    f"Note at position {note_index} for ticket "
                    f"'{ticket_id}' has an invalid note ID format."
                )

            if note_id in seen_note_ids:
                raise ValueError(
                    f"Duplicate note ID '{note_id}' for ticket "
                    f"'{ticket_id}'."
                )

            seen_note_ids.add(note_id)

            author = note.get("author")

            if not isinstance(author, str) or not author.strip():
                raise ValueError(
                    f"Note '{note_id}' for ticket '{ticket_id}' "
                    "must have a non-empty author."
                )

            message = note.get("message")

            if not isinstance(message, str):
                raise ValueError(
                    f"Note '{note_id}' for ticket '{ticket_id}' "
                    "must have a string message."
                )

            if not 5 <= len(message.strip()) <= 300:
                raise ValueError(
                    f"Note '{note_id}' for ticket '{ticket_id}' "
                    "must have a message containing 5 to 300 characters."
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
