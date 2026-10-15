"""CLI menus for searching tickets, reports, and ticket notes."""

from campusflow.notes import add_note, list_notes
from campusflow.reports import generate_report
from campusflow.search import search_tickets, sort_search_results_by_priority


def _ask_filter(label, valid_options, input_fn=input, output_fn=print):
    """Ask for an optional filter and validate the response."""

    while True:
        answer = input_fn(
            f"{label} ({'/'.join(valid_options)}, or Enter to skip): "
        ).strip()

        if not answer:
            return None

        for option in valid_options:
            if answer.casefold() == option.casefold():
                return option

        output_fn(
            f"Invalid {label.lower()}. Choose one of: "
            f"{', '.join(valid_options)}."
        )

def search_menu(tickets, input_fn=input, output_fn=print):
    """Search tickets using optional filters."""

    output_fn("\n--- Search Tickets ---")

    title = input_fn("Title keyword (or Enter to skip): ").strip()

    category = _ask_filter(
        "Category",
        ["network", "hardware", "software", "other"],
        input_fn,
        output_fn,
    )

    status = _ask_filter(
        "Status",
        ["open", "in_progress", "resolved"],
        input_fn,
        output_fn,
    )

    priority = _ask_filter(
        "Priority",
        ["critical", "high", "medium", "low"],
        input_fn,
        output_fn,
    )

    results = search_tickets(
        tickets,
        title=title,
        category=category,
        status=status,
        priority=priority,
    )

    results = sort_search_results_by_priority(results)

    if not results:
        output_fn("No matching tickets found.")
        return results

    output_fn(f"\nFound {len(results)} matching ticket(s):")

    for ticket in results:
        output_fn(
            f'{ticket.get("id", "Unknown ID")} | '
            f'{ticket.get("title", "Untitled")} | '
            f'{ticket.get("category", "Uncategorized")} | '
            f'{ticket.get("status", "Unknown")} | '
            f'{ticket.get("priority", "Unknown")}'
        )

    return results


def reports_menu(tickets, output_fn=print):
    """Display the ticket summary report."""

    report = generate_report(tickets)

    output_fn("\n--- Ticket Report ---")
    output_fn(f'Total tickets: {report["total"]}')
    output_fn(f'Unresolved tickets: {report["unresolved"]}')
    output_fn(f'Resolved tickets: {report["resolved"]}')
    output_fn(
        f'Resolution percentage: {report["resolution_percentage"]:.2f}%'
    )

    output_fn("\nTickets by status:")

    for status, count in report["by_status"].items():
        output_fn(f"  {status}: {count}")

    output_fn("\nTickets by priority:")

    for priority, count in report["by_priority"].items():
        output_fn(f"  {priority}: {count}")

    output_fn("\nTickets by category:")

    for category, count in report["by_category"].items():
        output_fn(f"  {category}: {count}")

    return report


def add_note_menu(tickets, save_fn, input_fn=input, output_fn=print):
    """Add a follow-up note to an existing ticket."""

    output_fn("\n--- Add Follow-up Note ---")

    ticket_id = input_fn("Ticket ID: ").strip()
    author = input_fn("Your name: ").strip()
    message = input_fn("Note: ").strip()

    note = add_note(tickets, ticket_id, author, message)

    save_fn(tickets)

    output_fn(
        f'Note {note["note_id"]} added successfully to ticket {ticket_id}.'
    )

    return note


def view_notes_menu(tickets, input_fn=input, output_fn=print):
    """Display notes associated with a ticket."""

    output_fn("\n--- View Ticket Notes ---")

    ticket_id = input_fn("Ticket ID: ").strip()

    notes = list_notes(tickets, ticket_id)

    if not notes:
        output_fn(f"No notes found for ticket {ticket_id}.")
        return notes

    def note_sort_key(note):
        note_id = str(note.get("note_id", ""))
        digits = "".join(character for character in note_id if character.isdigit())
        return (int(digits) if digits else float("inf"), note_id)

    notes = sorted(notes, key=note_sort_key)

    output_fn(f"\nNotes for ticket {ticket_id}:")

    for note in notes:
        output_fn(
            f'Note {note.get("note_id", "Unknown")} | '
            f'{note.get("author", "Unknown author")} | '
            f'{note.get("message", "")}'
        )

    return notes
