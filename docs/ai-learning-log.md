# AI-Assisted Learning Log — CampusFlow

## Engineer Role
Engineer A — Ticket Creation and Priority Calculation

## Project Overview
CampusFlow is a Python command-line campus helpdesk ticket manager designed to record campus technical issues, calculate ticket priorities, and support helpdesk ticket management.

## My Contribution
I developed the ticket creation module in `campusflow/tickets.py`.

My implementation includes:
- Creating tickets with validated input.
- Generating sequential ticket IDs such as T001 and T002.
- Calculating ticket priority from urgency and affected users.
- Setting each new ticket's status to `open`.
- Setting `assigned_to` to `None` for new tickets.
- Rejecting invalid titles, categories, urgency values, and affected-user counts.

## Use of AI Assistance
I used AI assistance to understand requirements, improve the implementation, identify edge cases, and develop automated tests.

I reviewed the suggested code, applied changes locally, and ran the tests to verify the ticket creation module.

## Testing
I wrote automated tests in `tests/test_tickets.py` using Python's `unittest` framework.

The tests cover:
- Critical, high, medium, and low priority calculations.
- Invalid urgency values.
- Invalid affected-user counts.
- Ticket creation and initial field values.
- Empty and incorrectly typed titles and categories.
- Sequential ticket ID generation.
- Handling of existing ticket IDs.
- Validation of the existing-ticket list.

Test command:

`python3 -m unittest discover -s tests -v`

Result: 17 tests passed.

## What I Learned
During this task, I improved my understanding of:
- Python functions and dictionaries.
- Input validation and exception handling.
- Conditional logic for priority calculation.
- Generating ticket identifiers.
- Writing automated unit tests.
- Using Git branches, commits, and pushes.
- Using AI assistance as a development aid and verifying code through testing.

## Current Limitations and Next Steps
- Ticket data persistence across program runs still needs to be implemented or integrated with the team's persistence solution.
- Integration with the workflow module needs to be verified.
- The team should confirm that the ticket priority rules match the agreed requirements.
- The team should review and merge this contribution through the existing pull request.

## Evidence of Testing
All 17 tests in `tests/test_tickets.py` passed during local testing.
