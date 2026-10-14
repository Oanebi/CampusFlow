
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

            with self.assertRaisesRegex(ValueError, "invalid JSON"):
                load_tickets(filename)

    def test_non_list_json_raises_error(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "tickets.json"
            filename.write_text(
                json.dumps({"id": "T001"}),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "JSON list"):
                load_tickets(filename)

    def test_non_dictionary_ticket_raises_error(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "tickets.json"
            filename.write_text(
                json.dumps([None]),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "JSON object"):
                load_tickets(filename)

    def test_ticket_without_id_raises_error(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "tickets.json"
            filename.write_text(
                json.dumps([{"title": "Wi-Fi failure"}]),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "ID"):
                load_tickets(filename)

    def test_duplicate_ticket_ids_raise_error(self):
        tickets = [
            {"id": "T001", "title": "Wi-Fi failure"},
            {"id": "T001", "title": "Broken projector"},
        ]

        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "tickets.json"
            filename.write_text(
                json.dumps(tickets),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Duplicate ticket ID"):
                load_tickets(filename)

    def test_saving_duplicate_ids_is_rejected(self):
        tickets = [
            {"id": "T001"},
            {"id": "T001"},
        ]

        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "tickets.json"
            filename.write_text(
                json.dumps([{"id": "T009"}]),
                encoding="utf-8",
            )

            original_contents = filename.read_text(encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Duplicate ticket ID"):
                save_tickets(tickets, filename)

            self.assertEqual(
                filename.read_text(encoding="utf-8"),
                original_contents,
            )

    def test_ticket_id_must_be_non_empty_string(self):
        for ticket_id in (None, "", "   ", 123):
            with self.subTest(ticket_id=ticket_id):
                with tempfile.TemporaryDirectory() as directory:
                    filename = Path(directory) / "tickets.json"
                    filename.write_text(
                        json.dumps([{"id": ticket_id}]),
                        encoding="utf-8",
                    )

                    with self.assertRaisesRegex(ValueError, "ID"):
                        load_tickets(filename)


    def test_save_and_load_ticket_notes(self):
        tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi failure",
                "priority": "high",
                "status": "open",
                "notes": [
                    {
                        "note_id": "N001",
                        "author": "Ada",
                        "message": "Router restarted",
                    }
                ],
            }
        ]

        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / "tickets.json"

            save_tickets(tickets, filename)
            loaded = load_tickets(filename)

            self.assertEqual(loaded, tickets)
            self.assertEqual(
                loaded[0]["notes"][0]["note_id"],
                "N001",
            )


if __name__ == "__main__":
    unittest.main()
