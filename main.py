from campusflow.tickets import create_ticket
from campusflow.workflow import (
    assign_ticket,
    update_ticket_status,
    get_work_queue,
    list_tickets,
    view_ticket,
)
from campusflow.storage import load_tickets, save_tickets
from campusflow.cli_features import (
    add_note_menu,
    reports_menu,
    search_menu,
    view_notes_menu,
)
from campusflow.understanding_check import run_quiz


def display_ticket(ticket):
    """Display a ticket's details."""
    print(f"\nTicket ID: {ticket['id']}")
    print(f"Title: {ticket['title']}")
    print(f"Category: {ticket['category']}")

    if ticket["category"].lower() == "other":
        print(
            f"Category details: "
            f"{ticket.get('category_details', 'Not specified')}"
        )

    print(f"Urgency: {ticket['urgency']}")
    print(f"Affected users: {ticket['affected_users']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Status: {ticket['status']}")
    print(f"Assigned to: {ticket['assigned_to'] or 'Unassigned'}")


def main():
    """Run the CampusFlow command-line application."""

    try:
        tickets = load_tickets()
    except (ValueError, OSError) as error:
        print(f"Could not load saved tickets: {error}")
        return

    print("Welcome to CampusFlow!")

    while True:
        print("\n--- CampusFlow Helpdesk ---")
        print("1. Create ticket")
        print("2. List tickets")
        print("3. View ticket")
        print("4. Assign ticket")
        print("5. Update ticket status")
        print("6. View work queue")
        print("7. View reports")
        print("8. Search tickets")
        print("9. Add follow-up note")
        print("10. View ticket notes")
        print("11. Engineering understanding check")
        print("12. Exit")

        choice = input("Choose an option (1-12): ").strip()

        try:
            if choice == "1":
                title = input("Ticket title: ").strip()

                category = input(
                    "Category (Network, Hardware, Software, Other): "
                ).strip()

                allowed_categories = {
                    "network",
                    "hardware",
                    "software",
                    "other",
                }

                if category.lower() not in allowed_categories:
                    raise ValueError(
                        "Category must be Network, Hardware, Software, or Other."
                    )

                category = category.title()
                category_details = None

                if category == "Other":
                    category_details = input(
                        "Please specify the problem category: "
                    ).strip()

                    while not category_details:
                        print("Category details cannot be empty.")
                        category_details = input(
                            "Please specify the problem category: "
                        ).strip()

                urgency = input(
                    "Urgency (low, medium, high): "
                ).strip().lower()

                affected_users = int(
                    input("Number of affected users: ").strip()
                )

                ticket = create_ticket(
                    title,
                    category,
                    urgency,
                    affected_users,
                    tickets,
                )

                if category == "Other":
                    ticket["category_details"] = category_details

                tickets.append(ticket)
                save_tickets(tickets)

                print(f"Ticket {ticket['id']} created successfully.")

            elif choice == "2":
                ticket_list = list_tickets(tickets)

                if not ticket_list:
                    print("No tickets found.")
                else:
                    for ticket in ticket_list:
                        display_ticket(ticket)

            elif choice == "3":
                ticket_id = input("Enter ticket ID: ").strip().upper()
                ticket = view_ticket(tickets, ticket_id)
                display_ticket(ticket)

            elif choice == "4":
                ticket_id = input("Enter ticket ID: ").strip().upper()
                staff_name = input("Enter staff name: ").strip()

                assign_ticket(tickets, ticket_id, staff_name)
                save_tickets(tickets)
                print(f"Ticket {ticket_id} assigned successfully.")

            elif choice == "5":
                ticket_id = input("Enter ticket ID: ").strip().upper()
                print("Available statuses: open, in_progress, resolved")
                new_status = input("Enter new status: ").strip().lower()

                update_ticket_status(tickets, ticket_id, new_status)
                save_tickets(tickets)
                print(f"Ticket {ticket_id} status updated to {new_status}.")

            elif choice == "6":
                queue = get_work_queue(tickets)

                if not queue:
                    print("The work queue is empty.")
                else:
                    print("\n--- Work Queue ---")
                    for ticket in queue:
                        display_ticket(ticket)

            elif choice == "7":
                reports_menu(tickets)

            elif choice == "8":
                search_menu(tickets)

            elif choice == "9":
                add_note_menu(tickets, save_tickets)

            elif choice == "10":
                view_notes_menu(tickets)

            elif choice == "11":
                run_quiz()

            elif choice == "12":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please choose a number from 1 to 12.")

        except (ValueError, TypeError) as error:
            print(f"Error: {error}")
        except OSError as error:
            print(f"File error: Could not save ticket data: {error}")


if __name__ == "__main__":
    main()
