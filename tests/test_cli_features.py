import unittest
from unittest.mock import Mock

from campusflow.cli_features import (
    _ask_filter,
    reports_menu,
    search_menu,
)


class TestCLIFeatures(unittest.TestCase):

    def test_invalid_filter_is_retried(self):
        input_fn = Mock(side_effect=["invalid", "Network"])
        output_fn = Mock()

        result = _ask_filter(
            "Category",
            ["Network", "Hardware", "Software", "Other"],
            input_fn,
            output_fn,
        )

        self.assertEqual(result, "Network")
        self.assertEqual(input_fn.call_count, 2)
        output_fn.assert_called_once()

    def test_empty_filter_means_no_filter(self):
        result = _ask_filter(
            "Status",
            ["open", "in_progress", "resolved"],
            input_fn=lambda prompt: "",
            output_fn=lambda message: None,
        )

        self.assertIsNone(result)

    def test_reports_menu_handles_empty_tickets(self):
        output_fn = Mock()

        report = reports_menu([], output_fn=output_fn)

        self.assertEqual(report["total"], 0)
        self.assertEqual(report["resolution_percentage"], 0)

        displayed_text = "\n".join(
            str(call.args[0])
            for call in output_fn.call_args_list
        )

        self.assertIn("Total tickets: 0", displayed_text)
        self.assertIn("Resolution percentage: 0.00%", displayed_text)

    def test_search_menu_displays_matching_ticket(self):
        tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi unavailable",
                "category": "Network",
                "priority": "high",
                "status": "open",
                "assigned_to": None,
            }
        ]

        inputs = iter(["wifi", "Network", "open", "high"])
        output_fn = Mock()

        results = search_menu(
            tickets,
            input_fn=lambda prompt: next(inputs),
            output_fn=output_fn,
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "T001")

        displayed_text = "\n".join(
            str(call.args[0])
            for call in output_fn.call_args_list
        )

        self.assertIn("T001", displayed_text)
        self.assertIn("Wi-Fi unavailable", displayed_text)


if __name__ == "__main__":
    unittest.main()
