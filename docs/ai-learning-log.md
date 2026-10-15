# AI-Assisted Learning Log — CampusFlow

## Engineer Role

Engineer A — Ticket Safety and Storage Engineer

## Project Overview

CampusFlow is a Python command-line campus helpdesk ticket manager designed to record campus technical issues, calculate ticket priorities, assign tickets to staff, track workflow status, manage follow-up notes, and retain ticket data using JSON storage.

## My Contributions

My contributions to CampusFlow include:

- Developing ticket creation and priority calculation in `campusflow/tickets.py`.
- Validating ticket titles, categories, urgency values, and affected-user counts.
- Generating ticket IDs while avoiding existing IDs.
- Strengthening workflow validation and ticket assignment rules.
- Implementing follow-up note functions in `campusflow/notes.py`.
- Adding and updating automated tests for notes and JSON persistence.
- Improving storage validation to reject invalid ticket and note data.
- Testing the implementation and using test failures to identify missing validation rules.

## Use of AI Assistance

I used AI assistance to understand project requirements, explore edge cases, review errors, and develop ideas for automated tests.

I tested suggested changes locally rather than assuming that AI-generated code was correct. For example, a test revealed that duplicate note IDs already present in a ticket's notes were not being rejected. I used that result to identify the missing validation, update the note ID generation logic, and rerun the relevant tests.

AI assistance helped me understand possible solutions, but I remained responsible for checking the implementation against the requirements and verifying its behaviour through testing.

## Learning Entry 1 — Input Validation and Priority Calculation

### Initial understanding gap

I needed to understand how to translate the project's priority rules into conditional logic and how to reject invalid input before creating a ticket.

### AI explanation and small example

AI assistance helped me understand why more specific conditions must be checked before broader conditions. For example, a high-urgency ticket affecting at least 10 users must receive critical priority before the general high-priority condition is evaluated.

A small, unrelated example of input validation is:

```python
def validate_age(age):
    if not isinstance(age, int) or isinstance(age, bool):
        raise ValueError("Age must be an integer.")

    if age < 0:
        raise ValueError("Age cannot be negative.")
```

This example shows how a function can reject invalid input instead of allowing it to continue through the program.

### Experiment and verification

I implemented ticket creation and priority calculation and ran the ticket tests:

```bash
python3 -m unittest discover -s tests -p "test_tickets.py" -v
```

The tests covered priority levels, invalid inputs, ticket fields, and ticket ID generation. My earlier recorded run reported 17 passing tests. The test suite was expanded as the implementation developed.

### What I learned

I learned that validation and conditional ordering both matter. Even when individual conditions are correct, checking them in the wrong order can produce an incorrect result. I also learned to test invalid values, not only normal inputs.

## Learning Entry 2 — Follow-up Notes and Unique IDs

### Initial understanding gap

I needed to understand how to add follow-up notes without overwriting existing notes and how to generate unique note IDs while accounting for IDs already present in the data.

### AI explanation and small example

AI assistance helped me understand how a list of dictionaries can represent multiple related records. Each note contains information such as its ID, author, and message.

A small, unrelated example of finding an unused identifier is:

```python
existing_ids = {"N001", "N002"}
number = 1

while f"N{number:03d}" in existing_ids:
    number += 1

next_id = f"N{number:03d}"
```

The loop checks existing identifiers before choosing the next available one.

### Experiment and verification

I added the `add_note()` and `list_notes()` functions and wrote tests for valid notes, invalid authors, message-length boundaries, resolved tickets, and note ID generation.

One test revealed that duplicate IDs already present in the notes list were not being rejected. I updated `_generate_note_id()` to check existing IDs and reran the notes test suite.

The subsequent notes test run reported 16 passing tests.

I also considered the importance of ensuring that a rejected note does not change the ticket's existing notes or consume an ID unnecessarily.

### What I learned

I learned that generating a new ID is only part of protecting data integrity. Existing data also needs to be checked, and failed operations should not leave behind partial changes. Tests should verify both the expected error and whether the data remains unchanged.

## Learning Entry 3 — JSON Persistence and Regression Testing

### Initial understanding gap

I needed to understand how to check that nested data, such as a ticket's follow-up notes, remains available after saving a ticket collection to JSON and loading it again.

### AI explanation and small example

JSON supports lists and dictionaries, so a ticket dictionary containing a list of note dictionaries can be saved and loaded as part of the same data structure.

A small, unrelated example is:

```python
import json

record = {
    "name": "Ada",
    "updates": ["Started", "Completed"]
}

encoded = json.dumps(record)
decoded = json.loads(encoded)

assert decoded == record
```

The assertion checks that the decoded value matches the original record.

### Experiment and verification

I added a storage test that saves a ticket containing a note to a temporary JSON file, loads it again, and compares the loaded data with the original data.

I also updated storage validation to check note IDs, authors, and message lengths, and added tests for duplicate note IDs, blank authors, and invalid messages.

The storage test suite reported 10 passing tests before the additional validation work. A subsequent full test run reported 67 passing tests.

### What I learned

I learned that successful saving and loading does not automatically mean the data is valid. Persistence tests check whether data can be retained and recovered, while validation tests check whether the data meets the project's rules.

I also learned the importance of regression testing: after changing one part of the application, I should rerun relevant tests and the full suite to check that existing behaviour still works.

## Critical Evaluation of AI Assistance

AI assistance was useful for explaining validation logic, suggesting edge cases, and helping me interpret test failures. However, an initially suggested implementation did not detect duplicate note IDs already present in the data.

The failing test exposed that gap. I used the failure to identify the missing check, updated the implementation, and reran the tests.

This experience taught me not to treat an AI suggestion as automatically correct. I need to compare proposed changes with the requirements, run tests locally, examine failures, and review the resulting code. Passing tests provide evidence for the cases covered by those tests, but they do not prove that every possible case is handled correctly.

## Git and Engineering Workflow

I used Git branches to separate development work from the main branch and pushed implementation work to the remote repository.

For the final contribution, I need to ensure that:

- My changes are committed with clear, descriptive commit messages.
- The complete test suite passes on the final version.
- The pull request explains the changes and includes relevant test results.
- My teammate reviews the contribution and provides substantive feedback.
- Any blocking review feedback is addressed before merging.
- The final integrated version is checked on the main branch.

The branch name and commit history should be confirmed using the current repository state rather than relying on an earlier record.

## Current Verification Status

My latest recorded full test run reported:

```text
Ran 67 tests
OK
```

This result applies to that particular test run. It should not be treated as confirmation that later changes have also passed.

I will rerun the full test suite after the final changes and update this section with the actual result. I will also verify the final Git status and confirm that the documented behaviour matches the implementation.

## Next Steps

- Review the final implementation and automated test coverage.
- Verify that ticket notes survive JSON save and reload.
- Confirm that invalid or duplicate note data is rejected as required.
- Check that failed operations leave existing data unchanged.
- Run the complete test suite after the final changes.
- Ensure the README and design decisions document match the actual implementation.
- Complete any required baseline testing and learning-log documentation.
- Submit the contribution for partner review, address feedback, and verify the final integrated version.
