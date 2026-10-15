# CampusFlow — Design Decisions

## 1. Overview

CampusFlow is a Python command-line helpdesk ticket manager designed to help a campus support team record technical issues, assign them to staff, track their progress, and identify which problems need attention first.

The goal is to keep the application small enough to build and understand within the team challenge, while still separating responsibilities and enforcing clear rules around ticket handling.

The application uses Python's standard library and JSON file storage rather than introducing a database or external framework. This keeps setup simple and makes the application easy to run, test, and extend.

## 2. Application Structure

The application is divided into modules according to responsibility:

| Module | Responsibility |
|---|---|
| `main.py` | Provides the command-line menu and connects user input to application functions. |
| `campusflow/tickets.py` | Creates tickets, validates core ticket fields, calculates priority, and generates ticket IDs. |
| `campusflow/workflow.py` | Handles ticket lookup, assignment, status transitions, listing, and work queue ordering. |
| `campusflow/notes.py` | Adds and retrieves ticket follow-up notes and generates note IDs. |
| `campusflow/reports.py` | Produces ticket summary reports. |
| `campusflow/storage.py` | Validates ticket and note data and saves tickets to or loads tickets from JSON. |
| `tests/` | Verifies expected behaviour, validation rules, and important edge cases. |

This separation keeps the command-line interface from owning the business rules. For example, workflow and note functions can be tested without asking a user to interact with the menu.

It also gives the team a clearer way to work in parallel: changes to reporting, notes, or storage can be developed without placing every responsibility in one large file.

## 3. Ticket Data Model

A ticket is represented as a Python dictionary with the following fields:

| Field | Purpose |
|---|---|
| `id` | Unique ticket identifier, such as `T001`. |
| `title` | Short description of the reported issue. |
| `category` | Type of issue, such as Network, Hardware, Software, or Other. |
| `urgency` | Reported urgency: low, medium, or high. |
| `affected_users` | Number of users experiencing the issue. |
| `priority` | Calculated priority used to order the work queue. |
| `status` | Current workflow state. |
| `assigned_to` | Staff member responsible for the ticket, or `None` if unassigned. |
| `notes` | A list of follow-up notes; older tickets may omit this field. |

Dictionaries provide a straightforward representation that works naturally with JSON. A dedicated class or database-backed model could offer stronger structure as the application grows, but would add complexity that is not necessary for the current scope.

## 4. Priority Calculation

Priority is calculated from two inputs: urgency and the number of affected users. The intention is to consider both how urgent an issue is and how broadly it affects the campus.

The rules are applied in this order:

| Condition | Result |
|---|---|
| High urgency and at least 10 affected users | Critical |
| High urgency, or at least 10 affected users | High |
| Medium urgency, or at least 3 affected users | Medium |
| All remaining valid combinations | Low |

The order matters. A ticket that meets the critical condition must be classified before the broader high-priority condition is checked.

Keeping this calculation in a dedicated function avoids duplicating the same rules in the CLI, reporting logic, or work queue. It also makes boundary conditions easier to test.

These thresholds are project rules, not a claim that they will fit every real helpdesk. A production system might make them configurable or revise them using operational feedback.

## 5. Ticket IDs

Tickets use identifiers in the form `T001`, `T002`, and so on. The identifier is separate from the ticket title, so users can refer to a ticket even when multiple issues have similar descriptions.

The ID generator checks existing ticket IDs and selects an unused identifier. This is important because ticket data can be loaded from a previous run rather than starting with an empty collection every time.

Storage validation rejects missing, invalid, or duplicate ticket IDs before data is saved or accepted after loading.

The current approach is suitable for this single-process application. If CampusFlow later supported multiple users creating tickets concurrently, ID generation would need stronger coordination to prevent collisions.

## 6. Workflow and State Transitions

Tickets follow three workflow states:

- `open` — the issue has been recorded and is awaiting work.
- `in_progress` — a staff member is working on the issue.
- `resolved` — the issue has been marked as resolved.

Assignment and status changes are governed by explicit rules. An unassigned ticket cannot move to `in_progress`. A resolved ticket must first be reopened to `open` before it can enter another state.

These restrictions help prevent the application from representing a ticket as actively being worked on when nobody is assigned, or from changing a resolved ticket without an explicit reopening step.

The workflow functions enforce these rules independently of the CLI. This means the same restrictions apply when the functions are called directly from tests or other parts of the application.

## 7. Work Queue Ordering

The work queue contains only tickets with `open` status, ordered by priority:

1. Critical
2. High
3. Medium
4. Low

When two tickets have the same priority, the ticket with the lower numeric ID comes first. For example, `T002` should appear before `T010`.

Resolved tickets and tickets already in progress are excluded because the queue is intended to show work awaiting action.

The queue is a view of the ticket collection; it does not need a separate persistent copy.

## 8. Ticket Follow-up Notes

Follow-up notes provide a way to record updates about work on a ticket without replacing the original ticket description.

The notes module exposes two main functions:

- `add_note(tickets, ticket_id, author, message)` — validates and adds a note to a ticket.
- `list_notes(tickets, ticket_id)` — retrieves a ticket's notes without modifying the ticket.

Each note is represented as a dictionary containing:

| Field | Purpose |
|---|---|
| `note_id` | Unique note identifier within its ticket, such as `N001`. |
| `author` | Name of the person adding the note. |
| `message` | Follow-up information about the ticket. |

Note IDs are generated independently for each ticket. Existing IDs are checked before generating the next available ID, and malformed or duplicate IDs are rejected.

An author must be a nonblank string. A note message must be a string containing between 5 and 300 characters after surrounding whitespace is removed.

Notes can be added only while a ticket is `open` or `in_progress`. A resolved ticket must be explicitly reopened before another note can be added.

Validation occurs before the ticket is modified. Invalid submissions must not add a note or consume a note ID.
**Safety and error handling**

The notes module validates the ticket, author, message, and ticket status before adding a note. Notes can be added only to tickets with `open` or `in_progress` status. A resolved ticket must be explicitly reopened before another note can be added.

The function should check existing note IDs before generating a new one. If validation fails, it should raise the agreed exception and leave the ticket's notes unchanged. Tests should verify both that the expected error is raised and that no partial change occurs.

The notes module provides the business logic for adding and listing notes, while the command-line interface handles user input and displays the results. The function signature and error-handling convention should be agreed with Engineer B and documented consistently.

## 9. Persistence with JSON

CampusFlow uses JSON to retain ticket data between application runs. The storage module provides separate functions for saving and loading the ticket collection.

JSON was chosen because it is readable, supported by Python's standard library, and sufficient for the project's small dataset. It also makes saved data easy to inspect during development and debugging.

The storage behaviour accounts for several cases:

- If the data file does not exist, the application starts with an empty ticket list.
- Valid JSON containing a list of tickets can be loaded.
- Malformed JSON produces a clear error instead of being silently treated as an empty dataset.
- JSON containing a top-level value other than a list is rejected.
- Ticket records must be dictionaries with valid, unique ticket IDs.
- If a ticket contains notes, the notes must have valid IDs, nonblank authors, and messages within the permitted length.
- Duplicate note IDs within the same ticket are rejected.
- Tickets without a `notes` field remain compatible with the application; the field is treated as an empty list when accessed by the notes and validation logic.

Because notes are stored inside their ticket dictionaries, they are saved and loaded along with the rest of the ticket data. This allows note history to remain available after the application restarts.

The current implementation is intentionally lightweight. It does not provide database transactions, multi-user locking, or automatic recovery from corrupted files.

## 10. Reporting

The reporting module produces an overall ticket count and breakdowns by status and priority.

Keeping reporting separate from the menu makes the counts reusable and testable without requiring terminal input. It also allows the CLI to focus on presenting the results rather than calculating them.

The empty-ticket case is handled so that a new installation can display a report with zero tickets instead of failing.

Additional breakdowns, such as category counts and resolution percentage, can be included as the reporting requirements demand.

## 11. Validation and Error Handling

Input validation prevents invalid ticket details, note records, and unsupported workflow operations from being accepted.

The application uses `ValueError` for invalid values and can catch expected errors at the CLI boundary to show readable messages instead of unnecessary tracebacks.

Storage errors are handled separately because a failure to read or write a file is different from entering an invalid ticket or note value.

Validation is performed before mutations where possible. For example, a note is checked before it is appended to a ticket, and ticket data is validated before a JSON file is opened for writing. This helps prevent invalid submissions from leaving partial changes.

The test suite verifies that rejected operations do not alter the relevant data in the cases covered by the tests.

## 12. Testing Strategy

The project uses Python's built-in `unittest` framework, avoiding additional test dependencies.

Tests cover ticket creation and priority calculation, validation, workflow transitions, assignment, queue ordering, reporting, follow-up notes, and JSON storage.

The notes tests cover valid note creation, author and message validation, message length boundaries, resolved-ticket restrictions, unknown tickets, unique note IDs, duplicate existing note IDs, and ensuring invalid submissions do not consume an ID.

Storage tests cover missing files, malformed JSON, invalid ticket records, duplicate ticket IDs, saving and loading tickets, and saving and loading ticket notes. Additional validation tests check that invalid note records are rejected.

At the latest recorded full-suite run, **67 tests passed** in the development environment. This is a useful verification point, but the full suite should be run again after subsequent changes and against the final integrated version on `main`.

## 13. Trade-offs and Future Improvements

The design favours simplicity, clear module boundaries, and testability over infrastructure that the current project does not need.

Possible future improvements include:

- Replacing dictionaries with a typed model or dataclass.
- Adding timestamps to notes and tickets.
- Expanding audit history for ticket changes.
- Supporting concurrent access safely if multiple processes use the same data.
- Introducing configurable priority thresholds.
- Expanding automated tests to cover CLI interaction and file-write failures.

These improvements are not assumed to exist in the current implementation. They represent possible next steps if the scope and reliability requirements of CampusFlow increase.

## 14. Conclusion

CampusFlow is designed around a small set of explicit rules: tickets have a consistent structure, priority is calculated predictably, workflow transitions are controlled, follow-up notes are validated, and saved data can be reused between runs.

The main engineering decision was to keep these rules separate from the user interface and storage layer. This makes the application easier to reason about, easier to test, and more practical for a small team to maintain within a limited development window.
