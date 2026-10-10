import unittest

from campusflow.tickets import (
    calculate_priority,
    create_ticket,
    generate_ticket_id,
)


class TestCalculatePriority(unittest.TestCase):

    def test_critical_priority(self):
        self.assertEqual(calculate_priority("high", 15), "critical")

    def test_high_priority_from_urgency(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_high_priority_from_affected_users(self):
        self.assertEqual(calculate_priority("low", 12), "high")

    def test_medium_priority(self):
        self.assertEqual(calculate_priority("medium", 5), "medium")

    def test_low_priority(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_invalid_urgency(self):
        with self.assertRaises(ValueError):
            calculate_priority("urgent", 5)

    def test_invalid_affected_users(self):
        for value in (0, -1, 2.5, True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    calculate_priority("high", value)


class TestCreateTicket(unittest.TestCase):

    def test_ticket_creation(self):
        ticket = create_ticket(
            "Wi-Fi failure",
            "Network",
            "high",
            15,
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_title_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            create_ticket("", "Network", "high", 5)

    def test_category_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            create_ticket("Wi-Fi failure", " ", "high", 5)

    def test_ticket_ids_are_generated_sequentially(self):
        tickets = []

        first = create_ticket(
            "Wi-Fi failure",
            "Network",
            "high",
            15,
            tickets,
        )
        tickets.append(first)

        second = create_ticket(
            "Broken projector",
            "Equipment",
            "medium",
            5,
            tickets,
        )
        tickets.append(second)

        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")

    def test_generate_id_skips_existing_ids(self):
        tickets = [
            {"id": "T001"},
            {"id": "T002"},
            {"id": "T004"},
        ]

        self.assertEqual(generate_ticket_id(tickets), "T003")

    # Five additional tests

    def test_title_must_be_a_string(self):
        with self.assertRaises(ValueError):
            create_ticket(123, "Network", "high", 5)

    def test_category_must_be_a_string(self):
        with self.assertRaises(ValueError):
            create_ticket("Wi-Fi failure", 123, "high", 5)

    def test_urgency_must_be_a_string(self):
        with self.assertRaises(ValueError):
            create_ticket("Wi-Fi failure", "Network", None, 5)

    def test_affected_users_must_be_positive_integer(self):
        for value in (0, -1, 2.5, True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    create_ticket(
                        "Wi-Fi failure",
                        "Network",
                        "high",
                        value,
                    )

    def test_existing_tickets_must_be_a_list(self):
        with self.assertRaises(ValueError):
            create_ticket(
                "Wi-Fi failure",
                "Network",
                "high",
                5,
                "not a list",
            )


if __name__ == "__main__":
    unittest.main()