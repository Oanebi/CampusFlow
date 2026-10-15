
"""Functions for adding and retrieving ticket follow-up notes."""

from campusflow.workflow import find_ticket


def _generate_note_id(notes):
    """Return the next available note ID for a ticket."""

    existing_ids = set()

    for note in notes:
        if not isinstance(note, dict):
            raise ValueError("Existing note data is invalid.")

        note_id = note.get("note_id")

        if not isinstance(note_id, str) or not note_id.startswith("N"):
            raise ValueError("Existing note ID is invalid.")

        number_part = note_id[1:]

        if not number_part.isdigit() or int(number_part) < 1:
            raise ValueError("Existing note ID is invalid.")

        # Require a consistent format, such as N001 or N012.
        if note_id != f"N{int(number_part):03d}":
            raise ValueError("Existing note ID format is invalid.")

        if note_id in existing_ids:
            raise ValueError(
                f"Duplicate note ID '{note_id}' in existing notes."
            )

        existing_ids.add(note_id)

    number = 1

    while f"N{number:03d}" in existing_ids:
        number += 1

    return f"N{number:03d}"


def add_note(tickets, ticket_id, author, message):
    """Validate and add a follow-up note to an eligible ticket."""

    ticket = find_ticket(tickets, ticket_id)

    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author must be a non-empty string.")

    if not isinstance(message, str):
        raise ValueError("Note message must be a string.")

    author = author.strip()
    message = message.strip()

    if not 5 <= len(message) <= 300:
        raise ValueError(
            "Note message must contain between 5 and 300 characters."
        )

    if ticket.get("status") not in ("open", "in_progress"):
        raise ValueError(
            "Notes can only be added to open or in-progress tickets."
        )

    existing_notes = ticket.get("notes", [])

    if not isinstance(existing_notes, list):
        raise ValueError("Existing ticket notes must be a list.")

    # Validate existing notes and generate an ID before changing the ticket.
    note_id = _generate_note_id(existing_notes)

    note = {
        "note_id": note_id,
        "author": author,
        "message": message,
    }

    if "notes" not in ticket:
        ticket["notes"] = []

    ticket["notes"].append(note)

    return note


def list_notes(tickets, ticket_id):
    """Return a copy of a ticket's notes without changing the ticket."""

    ticket = find_ticket(tickets, ticket_id)
    notes = ticket.get("notes", [])

    if not isinstance(notes, list):
        raise ValueError("Existing ticket notes must be a list.")

    return list(notes)