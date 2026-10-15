import unittest

from campusflow.search import (
    search_tickets,
    sort_search_results_by_priority,
)


class TestSearchTickets(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T010",
                "title": "Wi-Fi router offline",
                "category": "Network",
                "status": "open",
                "priority": "high",
            },
            {
                "id": "T002",
                "title": "Wi-Fi connection restored",
                "category": "Network",
                "status": "resolved",
                "priority": "low",
            },
            {
                "id": "T003",
                "title": "Laptop screen broken",
                "category": "Hardware",
                "status": "open",
                "priority": "critical",
            },
            {
                "id": "T001",
                "title": "Wi-Fi access point failed",
                "category": "Network",
                "status": "open",
                "priority": "critical",
            },
        ]

    def test_title_search_ignores_case(self):
        results = search_tickets(self.tickets, title="WIFI")
        self.assertEqual(len(results), 3)

    def test_combined_filters_use_and(self):
        results = search_tickets(
            self.tickets,
            title="wifi",
            category="Network",
            status="open",
            priority="high",
        )
        self.assertEqual([ticket["id"] for ticket in results], ["T010"])

    def test_category_filter(self):
        results = search_tickets(self.tickets, category="hardware")
        self.assertEqual([ticket["id"] for ticket in results], ["T003"])

    def test_status_filter(self):
        results = search_tickets(self.tickets, status="resolved")
        self.assertEqual([ticket["id"] for ticket in results], ["T002"])

    def test_priority_filter(self):
        results = search_tickets(self.tickets, priority="critical")
        self.assertEqual(
            {ticket["id"] for ticket in results},
            {"T003", "T001"},
        )

    def test_no_matches_returns_empty_list(self):
        results = search_tickets(self.tickets, title="printer")
        self.assertEqual(results, [])

    def test_search_does_not_modify_tickets(self):
        before = [ticket.copy() for ticket in self.tickets]
        search_tickets(
            self.tickets,
            title="wifi",
            category="Network",
            status="open",
        )
        self.assertEqual(self.tickets, before)

    def test_priority_sorting_returns_sorted_copy(self):
        original = list(self.tickets)
        results = sort_search_results_by_priority(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001", "T003", "T010", "T002"],
        )
        self.assertEqual(self.tickets, original)
        self.assertIsNot(results, self.tickets)

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, status="waiting")


if __name__ == "__main__":
    unittest.main()
