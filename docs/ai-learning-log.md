# AI-Assisted Learning Log — CampusFlow

## Engineer Role

Engineer A — Ticket Creation, Priority Calculation, and Reliability

## Project Overview

CampusFlow is a Python command-line campus helpdesk ticket manager designed to record campus technical issues, calculate ticket priorities, assign tickets to staff, track workflow status, and retain ticket data using JSON storage.

## My Contributions

My work includes:

- Developing ticket creation and priority calculation in `campusflow/tickets.py`.
- Validating ticket titles, categories, urgency values, and affected-user counts.
- Generating ticket IDs while avoiding existing IDs.
- Strengthening workflow validation and ticket assignment rules.
- Implementing follow-up note functions in `campusflow/notes.py`.
- Adding and updating automated tests for notes and JSON persistence.
- Improving storage validation to reject invalid ticket and note data.

## Use of AI Assistance

I used AI assistance to help understand requirements, explore edge cases, review errors, and develop test cases.

I ran the suggested code and tests locally and used the results to identify problems. One example was a test that detected that duplicate existing note IDs were not being rejected. I updated the note ID generation logic and reran the notes tests.

AI-generated suggestions were treated as proposals to check, not as proof that the implementation was correct. Test results provided evidence for the specific cases covered, but they did not prove that every possible case was handled correctly.

## Learning Entry 1 — Input Validation and Priority Calculation

### Initial understanding gap

I needed to understand how to turn the priority rules into conditional logic and how to reject invalid input before creating a ticket.

### AI explanation and small example

AI assistance helped me reason about checking the most specific priority condition first. For example, a high-urgency ticket affecting at least 10 users must be classified as critical before the broader high-priority condition is checked.

A small unrelated example of validation is:

```python
def validate_age(age):
    if not isinstance(age, int) or isinstance(age, bool):
        raise ValueError("Age must be an integer.")
    if age < 0:
        raise ValueError("Age cannot be negative.")
```

The example shows how validation prevents invalid values from being accepted.

### Experiment and verification

I implemented ticket creation and priority calculation and ran the ticket tests:

```bash
python3 -m unittest discover -s tests -p "test_tickets.py" -v
```

The tests covered priority levels, invalid inputs, ticket fields, and ticket ID generation. My earlier recorded run reported 17 passing tests. I later expanded the project test suite as the implementation developed.

### What I learned

I learned that validation and conditional ordering matter. A correct priority rule can produce the wrong result if a broader condition is checked before a more specific one.

## Learning Entry 2 — Follow-up Notes and Unique IDs

### Initial understanding gap

I needed to understand how to add follow-up notes to a ticket without overwriting existing notes, and how to generate a new note ID without duplicating an existing one.

### AI explanation and small example

AI assistance helped me understand the use of a list of dictionaries to store related records. Each note contains a note ID, author, and message.

A small unrelated example of finding an unused identifier is:

```python
existing_ids = {"N001", "N002"}
number = 1

while f"N{number:03d}" in existing_ids:
    number += 1

next_id = f"N{number:03d}"
```

The loop checks existing identifiers before choosing a new one.

### Experiment and verification

I added the `add_note()` and `list_notes()` functions and wrote tests for valid notes, invalid authors, message-length boundaries, resolved tickets, and note IDs.

One test revealed that duplicate IDs already present in the notes list were not rejected. I changed `_generate_note_id()` to check for duplicate existing IDs and reran the notes test suite.

The notes suite subsequently reported 16 passing tests.

### What I learned

I learned that generating a new unique ID is not enough by itself. Existing data must also be checked for duplicates or invalid identifiers before a new note is added.

## Learning Entry 3 — JSON Persistence and Regression Testing

### Initial understanding gap

I needed to understand how to verify that nested data, such as a ticket's notes, remains available after the ticket collection is saved to JSON and loaded again.

### AI explanation and small example

JSON can represent lists and dictionaries, so a ticket dictionary containing a list of note dictionaries can be saved and loaded as a whole.

A small unrelated example is:

```python
import json

record = {"name": "Ada", "updates": ["Started", "Completed"]}

encoded = json.dumps(record)
decoded = json.loads(encoded)

assert decoded == record
```

The assertion checks that the decoded data matches the original data.

### Experiment and verification

I added a storage test that saves a ticket containing a note to a temporary JSON file, loads it, and checks that the saved data matches the original data.

I also updated storage validation to check note IDs, authors, and message lengths, and added tests for duplicate note IDs, blank authors, and invalid messages.

The storage test suite reported 10 passing tests before the additional validation tests. The subsequent full test run reported 67 passing tests.

### What I learned

I learned that saving and loading data successfully does not automatically mean that the data is valid. Persistence tests and validation tests check different aspects of reliability.

## Critical Evaluation of AI Assistance

AI assistance was useful for explaining validation logic, suggesting edge cases, and helping me interpret test failures. However, an initially suggested implementation did not detect duplicate note IDs already present in the data.

The failing test exposed that gap. I used the failure to identify the missing check, updated the implementation, and reran the tests.

This experience showed me why AI-generated code needs to be reviewed and tested locally. Passing tests provide evidence that the tested cases work, but additional tests and code review are still necessary.

## Git and Engineering Workflow

I worked on the `feature/engineer-a-reliability` branch and pushed an earlier implementation commit to the remote repository.

Before the final pull request, I need to verify the current Git status, review the latest changes, run the complete test suite, and ensure the final contribution is submitted through the team's agreed pull-request review process.

## Current Verification Status

The latest full test output I recorded reported:

```text
Ran 67 tests
OK
```

This result applies to that particular run. I will rerun the full suite after the final changes and record the new result if the test count changes.

## Next Steps

- Review the final implementation and test coverage.
- Verify that notes survive JSON save/reload and that invalid note data is rejected.
- Run the complete test suite after the final changes.
- Update the project documentation to match the implementation.
- Submit the contribution for partner review and address any review feedback.
