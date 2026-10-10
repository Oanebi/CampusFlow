
import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import save_tickets, load_tickets


class TestStorage(unittest.TestCase):

    def test_save_and_load_tickets(self):
        tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi failure",
                "priority": "high",
                "status": "open",
            }
        ]

        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "tickets.json"

            save_tickets(tickets, filename)
            loaded = load_tickets(filename)

            self.assertEqual(loaded, tickets)

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "missing.json"

            self.assertEqual(load_tickets(filename), [])

    def test_invalid_json_raises_error(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "tickets.json"
            filename.write_text("{invalid json", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tickets(filename)

    def test_non_list_json_raises_error(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "tickets.json"
            filename.write_text(
                json.dumps({"id": "T001"}),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_tickets(filename)


if __name__ == "__main__":
    unittest.main()
