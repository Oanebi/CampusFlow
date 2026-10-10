# CampusFlow — Design Decisions

## 1. Overview

CampusFlow is a Python command-line helpdesk ticket manager designed to help a campus support team record technical issues, assign them to staff, track their progress, and identify which problems need attention first.

The goal was to keep the application small enough to build and understand within the team challenge, while still separating responsibilities and enforcing clear rules around ticket handling.

Rather than introducing a database or external framework, the project uses Python's standard library and JSON file storage. This keeps the setup simple and makes the application easy to run, test, and extend.

## 2. Application Structure

The application is divided into modules according to responsibility:

| Module | Responsibility |
|---|---|
| `main.py` | Provides the command-line menu and connects user input to application functions. |
| `campusflow/tickets.py` | Creates tickets, validates core ticket fields, calculates priority, and generates ticket IDs. |
| `campusflow/workflow.py` | Handles ticket lookup, assignment, status transitions, listing, and work queue ordering. |
| `campusflow/reports.py` | Produces summary counts for ticket statuses and priorities. |
| `campusflow/storage.py` | Saves tickets to JSON and loads previously saved tickets. |
| `tests/` | Verifies expected behaviour, validation rules, and important edge cases. |

This separation keeps the command-line interface from owning the business rules. For example, the workflow logic can be tested without asking a user to interact with the menu.

It also gives the team a clearer way to work in parallel: changes to reporting or storage can be developed without placing every responsibility in one large file.

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

For this version, dictionaries provide a straightforward representation that works naturally with JSON. A dedicated class or database-backed model could offer stronger structure as the application grows, but would add complexity that is not necessary for the current scope.

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

The ID generator checks the existing ticket IDs and selects an unused identifier. This is important because ticket data can be loaded from a previous run rather than starting with an empty collection every time.

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

The work queue places unresolved tickets in this priority order:

1. Critical
2. High
3. Medium
4. Low

When two tickets have the same priority, the ticket with the lower numeric ID comes first. For example, `T002` should appear before `T010`.

Resolved tickets are excluded because they no longer require active work.

This gives the support team a predictable queue and avoids relying on the order in which tickets happen to appear in the saved JSON file. The queue is a view of the ticket collection; it does not need a separate persistent copy.

## 8. Persistence with JSON

CampusFlow uses JSON to retain ticket data between application runs. The storage module provides separate functions for saving and loading the ticket collection.

JSON was chosen because it is readable, supported by Python's standard library, and sufficient for the project's small dataset. It also makes saved data easy to inspect during development and debugging.

The storage behaviour accounts for several cases:

- If the data file does not exist, the application starts with an empty ticket list.
- Valid JSON containing a list can be loaded into the application.
- Malformed JSON produces a clear error instead of being silently treated as an empty dataset.
- JSON containing a top-level value other than a list is rejected.

The current implementation is intentionally lightweight. It does not provide database transactions, multi-user locking, or automatic recovery from corrupted files. Those would become relevant if the application were used with more demanding reliability requirements.

## 9. Reporting

The reporting module produces an overall ticket count and breakdowns by status and priority.

Keeping reporting separate from the menu makes the counts reusable and testable without requiring terminal input. It also allows the CLI to focus on presenting the results rather than calculating them.

The empty-ticket case is handled so that a new installation can display a report with zero tickets instead of failing.

## 10. Validation and Error Handling

Input validation is used to prevent invalid ticket details and unsupported workflow operations from being accepted.

The application uses `ValueError` for invalid values and catches expected errors at the CLI boundary so that a user can receive a readable message instead of an unnecessary traceback.

Storage errors are handled separately because a failure to read or write a file is different from entering an invalid ticket value.

This approach keeps the core functions responsible for enforcing rules while allowing the CLI to decide how errors are presented. It also gives the test suite a clear way to verify rejected operations.

## 11. Testing Strategy

The project uses Python's built-in `unittest` framework, avoiding additional test dependencies.

Tests cover ticket creation and priority calculation, validation, workflow transitions, assignment, queue ordering, reporting, and JSON storage. Particular attention is given to boundary conditions and invalid operations, since these are common sources of mistakes in ticket-management systems.

The full test suite currently passes 39 tests in the development environment. That result is a useful verification point, although it does not replace manual checks of the complete CLI or a fresh test run after the final changes are integrated into `main`.

## 12. Trade-offs and Future Improvements

The design favours simplicity, clear module boundaries, and testability over infrastructure that the current project does not need.

Possible future improvements include:

- Replacing dictionaries with a typed model or dataclass.
- Adding stronger validation when loading individual records from JSON.
- Supporting concurrent access safely if multiple processes use the same data.
- Introducing configurable priority thresholds.
- Adding timestamps, audit history, and more detailed reporting.
- Expanding automated tests to cover CLI interaction and file-write failures.

These improvements are not assumed to exist in the current implementation. They represent possible next steps if the scope and reliability requirements of CampusFlow increase.

## 13. Conclusion

CampusFlow is designed around a small set of explicit rules: tickets have a consistent structure, priority is calculated predictably, workflow transitions are controlled, and saved data can be reused between runs.

The main engineering decision was to keep those rules separate from the user interface and storage layer. This makes the application easier to reason about, easier to test, and more practical for a small team to maintain within a limited development window.