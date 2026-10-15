import unittest

from campusflow.notes import add_note, list_notes


class TestTicketNotes(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Wi-Fi failure",
                "status": "open",
                "assigned_to": None,
            },
            {
                "id": "T002",
                "title": "Broken projector",
                "status": "in_progress",
                "assigned_to": "Ada",
                "notes": [],
            },
            {
                "id": "T003",
                "title": "Old network issue",
                "status": "resolved",
                "assigned_to": "Ada",
                "notes": [],
            },
        ]

    def test_add_note_to_open_ticket(self):
        note = add_note(
            self.tickets, "T001", "Ada", "Router restarted"
        )

        self.assertEqual(
            note,
            {
                "note_id": "N001",
                "author": "Ada",
                "message": "Router restarted",
            },
        )
        self.assertEqual(self.tickets[0]["notes"], [note])

    def test_add_note_to_in_progress_ticket(self):
        note = add_note(
            self.tickets, "T002", "Ada", "Checking the network"
        )

        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(len(self.tickets[1]["notes"]), 1)

    def test_list_notes_for_ticket_without_notes(self):
        self.assertEqual(list_notes(self.tickets, "T001"), [])

    def test_list_notes_returns_existing_notes(self):
        add_note(self.tickets, "T001", "Ada", "Router restarted")

        notes = list_notes(self.tickets, "T001")

        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["author"], "Ada")

    def test_note_ids_are_unique_within_ticket(self):
        first = add_note(
            self.tickets, "T001", "Ada", "First update"
        )
        second = add_note(
            self.tickets, "T001", "Ben", "Second update"
        )

        self.assertEqual(first["note_id"], "N001")
        self.assertEqual(second["note_id"], "N002")

    def test_note_ids_are_independent_per_ticket(self):
        first = add_note(
            self.tickets, "T001", "Ada", "First update"
        )
        second = add_note(
            self.tickets, "T002", "Ben", "Second update"
        )

        self.assertEqual(first["note_id"], "N001")
        self.assertEqual(second["note_id"], "N001")

    def test_note_id_skips_existing_id(self):
        self.tickets[0]["notes"] = [
            {
                "note_id": "N001",
                "author": "Ada",
                "message": "Earlier update",
            },
            {
                "note_id": "N003",
                "author": "Ben",
                "message": "Another update",
            },
        ]

        note = add_note(
            self.tickets, "T001", "Ada", "Latest update"
        )

        self.assertEqual(note["note_id"], "N002")

    def test_blank_author_is_rejected_without_changes(self):
        before = [dict(ticket) for ticket in self.tickets]

        for author in ("", "   ", None, 123):
            with self.subTest(author=author):
                with self.assertRaises(ValueError):
                    add_note(
                        self.tickets,
                        "T001",
                        author,
                        "Valid message",
                    )

        self.assertEqual(self.tickets, before)

    def test_invalid_message_is_rejected_without_changes(self):
        before = [dict(ticket) for ticket in self.tickets]

        invalid_messages = ("", "   ", "abcd", "x" * 301, None, 123)

        for message in invalid_messages:
            with self.subTest(message=message):
                with self.assertRaises(ValueError):
                    add_note(
                        self.tickets, "T001", "Ada", message
                    )

        self.assertEqual(self.tickets, before)

    def test_message_boundaries_are_accepted(self):
        short_note = add_note(
            self.tickets, "T001", "Ada", "12345"
        )
        long_note = add_note(
            self.tickets, "T001", "Ada", "x" * 300
        )

        self.assertEqual(len(short_note["message"]), 5)
        self.assertEqual(len(long_note["message"]), 300)

    def test_resolved_ticket_rejects_note(self):
        before = dict(self.tickets[2])

        with self.assertRaises(ValueError):
            add_note(
                self.tickets,
                "T003",
                "Ada",
                "Follow-up update",
            )

        self.assertEqual(self.tickets[2], before)

    def test_reopened_ticket_accepts_note(self):
        self.tickets[2]["status"] = "open"

        note = add_note(
            self.tickets, "T003", "Ada", "Follow-up update"
        )

        self.assertEqual(note["note_id"], "N001")

    def test_unknown_ticket_is_rejected(self):
        with self.assertRaises(ValueError):
            add_note(
                self.tickets, "T999", "Ada", "Valid message"
            )

    def test_invalid_note_does_not_consume_id(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", " ", "Valid message")

        note = add_note(
            self.tickets, "T001", "Ada", "Valid message"
        )

        self.assertEqual(note["note_id"], "N001")

    def test_duplicate_existing_note_ids_are_not_generated(self):
        self.tickets[0]["notes"] = [
            {
                "note_id": "N001",
                "author": "Ada",
                "message": "First note",
            },
            {
                "note_id": "N001",
                "author": "Ben",
                "message": "Duplicate note",
            },
        ]

        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Ada", "New update")

    def test_list_notes_does_not_modify_ticket(self):
        add_note(self.tickets, "T001", "Ada", "Valid message")
        before = [dict(ticket) for ticket in self.tickets]

        list_notes(self.tickets, "T001")

        self.assertEqual(self.tickets, before)


if __name__ == "__main__":
    unittest.main()
