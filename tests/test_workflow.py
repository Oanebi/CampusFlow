
import unittest

from campusflow.workflow import (
    find_ticket,
    assign_ticket,
    update_ticket_status,
    get_work_queue,
    list_tickets,
    view_ticket,
)


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi failure",
                "priority": "high",
                "status": "open",
            },
            {
                "id": "T002",
                "title": "Broken projector",
                "priority": "medium",
                "status": "in_progress",
                "assigned_to": "Ada",
            },
        ]

    def test_find_existing_ticket(self):
        ticket = find_ticket(self.tickets, "T002")
        self.assertEqual(ticket["id"], "T002")

    def test_unknown_ticket_raises_error(self):
        with self.assertRaises(ValueError):
            find_ticket(self.tickets, "T999")

    def test_assign_ticket(self):
        ticket = assign_ticket(self.tickets, "T001", " Ada ")
        self.assertEqual(ticket["assigned_to"], "Ada")

    def test_assign_ticket_rejects_empty_staff_name(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")

    def test_assign_ticket_rejects_unknown_ticket(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "Ada")

    def test_unassigned_ticket_cannot_start(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.tickets, "T001", "in_progress")

        self.assertEqual(self.tickets[0]["status"], "open")

    def test_assigned_ticket_can_start(self):
        assign_ticket(self.tickets, "T001", "Ada")
        ticket = update_ticket_status(
            self.tickets, "T001", "in_progress"
        )
        self.assertEqual(ticket["status"], "in_progress")

    def test_in_progress_ticket_can_be_resolved(self):
        ticket = update_ticket_status(
            self.tickets, "T002", "resolved"
        )
        self.assertEqual(ticket["status"], "resolved")

    def test_resolved_ticket_must_be_reopened(self):
        self.tickets[0]["status"] = "resolved"

        with self.assertRaises(ValueError):
            update_ticket_status(self.tickets, "T001", "in_progress")

        ticket = update_ticket_status(self.tickets, "T001", "open")
        self.assertEqual(ticket["status"], "open")

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.tickets, "T001", "waiting")

    def test_queue_sorts_by_priority(self):
        tickets = [
            {"id": "T001", "priority": "low", "status": "open"},
            {"id": "T002", "priority": "critical", "status": "open"},
            {"id": "T003", "priority": "high", "status": "in_progress"},
            {"id": "T004", "priority": "medium", "status": "open"},
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T003", "T004", "T001"],
        )

    def test_queue_excludes_resolved_tickets(self):
        tickets = [
            {"id": "T001", "priority": "critical", "status": "resolved"},
            {"id": "T002", "priority": "low", "status": "open"},
        ]

        queue = get_work_queue(tickets)

        self.assertEqual([ticket["id"] for ticket in queue], ["T002"])

    def test_queue_breaks_priority_ties_numerically(self):
        tickets = [
            {"id": "T010", "priority": "high", "status": "open"},
            {"id": "T002", "priority": "high", "status": "open"},
            {"id": "T001", "priority": "high", "status": "open"},
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T001", "T002", "T010"],
        )

    def test_list_tickets(self):
        result = list_tickets(self.tickets)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "T001")

    def test_view_ticket(self):
        ticket = view_ticket(self.tickets, "T002")
        self.assertEqual(ticket["title"], "Broken projector")

    def test_view_unknown_ticket(self):
        with self.assertRaises(ValueError):
            view_ticket(self.tickets, "T999")


if __name__ == "__main__":
    unittest.main()
