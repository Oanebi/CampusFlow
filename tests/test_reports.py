import unittest

from campusflow.reports import generate_report


class TestGenerateReport(unittest.TestCase):

    def test_report_counts_tickets(self):
        tickets = [
            {
                "id": "T001",
                "status": "open",
                "priority": "high",
                "category": "Network",
            },
            {
                "id": "T002",
                "status": "resolved",
                "priority": "low",
                "category": "Hardware",
            },
            {
                "id": "T003",
                "status": "open",
                "priority": "critical",
                "category": "Network",
            },
        ]

        report = generate_report(tickets)

        self.assertEqual(report["total"], 3)

        self.assertEqual(report["by_status"]["open"], 2)
        self.assertEqual(report["by_status"]["resolved"], 1)

        self.assertEqual(report["by_priority"]["high"], 1)
        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_priority"]["low"], 1)

        self.assertEqual(report["by_category"]["Network"], 2)
        self.assertEqual(report["by_category"]["Hardware"], 1)

        self.assertEqual(report["unresolved"], 2)
        self.assertEqual(report["resolved"], 1)

        self.assertAlmostEqual(
            report["resolution_percentage"],
            33.33,
            places=2,
        )

    def test_empty_ticket_list(self):
        report = generate_report([])

        self.assertEqual(report["total"], 0)
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["resolution_percentage"], 0)

        self.assertEqual(report["by_status"]["open"], 0)
        self.assertEqual(report["by_status"]["in_progress"], 0)
        self.assertEqual(report["by_status"]["resolved"], 0)

        self.assertEqual(report["by_priority"]["critical"], 0)
        self.assertEqual(report["by_category"], {})

    def test_in_progress_tickets_are_unresolved(self):
        tickets = [
            {
                "id": "T001",
                "status": "in_progress",
                "priority": "medium",
                "category": "Software",
            },
            {
                "id": "T002",
                "status": "resolved",
                "priority": "high",
                "category": "Network",
            },
        ]

        report = generate_report(tickets)

        self.assertEqual(report["unresolved"], 1)
        self.assertEqual(report["resolved"], 1)
        self.assertEqual(report["resolution_percentage"], 50)

    def test_reopened_ticket_uses_current_status(self):
        tickets = [
            {
                "id": "T001",
                "status": "open",
                "priority": "high",
                "category": "Network",
            },
        ]

        report = generate_report(tickets)

        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["unresolved"], 1)
        self.assertEqual(report["resolution_percentage"], 0)

    def test_missing_category_is_counted_as_uncategorized(self):
        tickets = [
            {
                "id": "T001",
                "status": "open",
                "priority": "low",
            },
        ]

        report = generate_report(tickets)

        self.assertEqual(report["by_category"]["Uncategorized"], 1)


if __name__ == "__main__":
    unittest.main()