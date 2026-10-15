# CampusFlow Baseline Check

## 1. Purpose

This document records the initial inspection and testing of CampusFlow, a Python command-line campus helpdesk ticket manager.

The purpose of the baseline check is to understand the application's existing behaviour, identify problems that can be reproduced, and distinguish confirmed defects from areas that still need investigation.

The baseline also provides a reference for evaluating changes made during development.

## 2. Project and Environment

- **Project:** CampusFlow
- **Language:** Python
- **Python version:** 3.12.3
- **Operating system:** Linux
- **Branch used for the current documentation work:** `docs/campusflow-documentation`
- **Test framework:** Python `unittest`
- **Storage format:** JSON
- **Baseline test date:** To be confirmed
- **Original implementation revision:** To be confirmed

The current branch contains documentation and notes-module changes. Therefore, test results from this branch must not automatically be treated as results from the original implementation.

## 3. Commands Used

### 3.1 Check the Python version

Command:

```bash
python3 --version
```

Recorded output:

```text
Python 3.12.3
```

**Result:** Python is available in the development environment.

### 3.2 Check the current Git branch and working tree

Commands:

```bash
git branch --show-current
git status
```

Recorded branch:

```text
docs/campusflow-documentation
```

The working tree contained modifications to `campusflow/notes.py`, `docs/ai-learning-log.md`, and `docs/design-decisions.md`. The file `docs/baseline-check.md` was untracked when the status command was run.

**Result:** The current documentation work is on a separate branch. The changes need to be reviewed and committed when they are ready.

### 3.3 Run the automated test suite

Command:

```bash
python3 -m unittest discover -s tests -v
```

A previously recorded run reported:

```text
Ran 67 tests
OK
```

**Result:** The recorded version passed 67 tests. This result applies to that particular run and does not establish the result of the original baseline or the latest uncommitted changes.

The complete test suite must be run again after the current changes are finished.

### 3.4 Start the command-line application

Command:

```bash
python3 main.py
```

The application has previously been observed to provide menu options for creating, listing, viewing, assigning, and updating tickets, viewing the work queue, and viewing reports.

**Result:** This behaviour was observed during earlier development. The application should be started again during final verification to confirm the current integrated version.

## 4. Representative Test Cases

The following cases describe the behaviours that should be checked. Actual results must be recorded after running each case against the version being assessed.

### Case 1 — Valid ticket creation

**Input:** A ticket with a non-empty title, a supported category, a valid urgency, and a positive integer for the number of affected users.

**Expected behaviour:**

- The application accepts the valid input.
- A unique ticket ID is generated.
- The ticket's priority is calculated according to the project rules.
- The new ticket is stored in the ticket collection.

**Actual behaviour:** To be recorded during the baseline check.

**Outcome:** Pending verification.

### Case 2 — Invalid ticket input

**Input:** Try an unsupported urgency, an invalid affected-user count, or a blank required field.

**Expected behaviour:**

- The application rejects the invalid input.
- A clear error is reported.
- No invalid ticket is added.
- Existing tickets remain unchanged.

**Actual behaviour:** To be recorded during the baseline check.

**Outcome:** Pending verification.

### Case 3 — Assignment and workflow validation

**Input:** Attempt to move an unassigned ticket into `in_progress`.

**Expected behaviour:** The application rejects the status change because the ticket has not been assigned.

**Additional check:** Attempt to modify a resolved ticket without explicitly reopening it.

**Expected behaviour:** The application rejects the prohibited change and preserves the ticket's existing state.

**Actual behaviour:** To be recorded during the baseline check.

**Outcome:** Pending verification.

### Case 4 — Follow-up note validation

**Input:** Attempt to add a note with a blank author, a message outside the permitted length, or a note on a resolved ticket.

**Expected behaviour:**

- Invalid authors and messages are rejected.
- Notes cannot be added to resolved tickets.
- Existing notes remain unchanged when a submission fails.
- A valid note receives an available note ID.

**Actual behaviour:** To be recorded during the baseline check.

**Outcome:** Pending verification.

### Case 5 — JSON save and reload

**Input:** Save a ticket collection containing at least one ticket with a follow-up note, then load it again.

**Expected behaviour:**

- The ticket data is saved successfully.
- The loaded data retains the ticket fields and its notes.
- Valid identifiers remain unchanged.
- Subsequent ID generation avoids IDs already in use.

**Additional check:** Attempt to load malformed JSON or data containing duplicate ticket IDs.

**Expected behaviour:** Invalid stored data is rejected with a clear error and is not silently accepted as valid data.

**Actual behaviour:** To be recorded during the baseline check.

**Outcome:** Pending verification.

## 5. Reproduced Problems

A problem should be listed here only when it has been reproduced through a manual check or supported by a failing test.

For each confirmed problem, record:

1. What action or input caused it.
2. What the application actually did.
3. What should have happened.
4. The command, test name, or steps used to reproduce it.
5. Whether the problem was fixed and retested.

| Problem | Evidence | Status |
|---|---|---|
| No original baseline defect confirmed in this document yet | Original test results and reproduction steps still need to be collected | Pending investigation |

This does not mean the original implementation had no defects. It means the available information is not sufficient to document a specific original defect as confirmed.

## 6. Unverified Items

The following items require evidence before conclusions can be made:

- Whether every original ticket-validation rule worked correctly.
- Whether invalid operations left the original ticket data unchanged.
- Whether duplicate or malformed note data was rejected by the original implementation.
- Whether JSON loading handled corrupted files safely.
- Whether ticket IDs remained correct after restarting the application.
- Whether all required search and combined-filter behaviours are implemented, if they are part of the final specification.
- Whether the final integrated version passes the complete test suite.

Unverified behaviour is not automatically a defect. It indicates that further testing or inspection is required.

## 7. Testing Approach

The baseline and subsequent regression checks should include:

- **Valid inputs:** Confirm that supported operations work as intended.
- **Invalid inputs:** Confirm that bad data is rejected.
- **Boundary values:** Test values at the limits of permitted ranges.
- **State preservation:** Compare the original data with the data after a rejected operation.
- **Persistence:** Save data, reload it, and compare the results.
- **Regression testing:** Rerun the complete test suite after changes.

Python's `unittest` framework is used for automated testing. Tests for rejected mutations should check both that the expected exception is raised and that the affected data remains unchanged.

## 8. Baseline Conclusion

The development environment has Python 3.12.3, and the current documentation work is on the `docs/campusflow-documentation` branch.

A previous full test run reported 67 passing tests. However, that result belongs to a particular development version and is not sufficient evidence of the original implementation's baseline behaviour.

The original baseline should be completed by running the relevant checks against the original revision, recording representative inputs and actual outcomes, and documenting only the problems that can be reproduced.

After implementation and documentation changes are complete, the full test suite and manual checks should be repeated on the integrated version. The final results should be recorded separately from the original baseline results.
