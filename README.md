# CampusFlow Next – Campus Helpdesk Ticket Management System

## 1. About the Project

CampusFlow Next is a Python command-line application designed to help students and staff report campus problems and help support staff manage them until they are resolved.

Examples include faulty laboratory computers, network failures, software problems, and electrical faults.

The application records reported problems as tickets, calculates priority, supports staff assignment, tracks ticket status, stores follow-up notes, and saves ticket data using JSON.

## 2. Project Objectives

CampusFlow Next aims to:

- Record campus problems in an organized way.
- Generate unique ticket IDs.
- Calculate ticket priority automatically.
- Assign tickets to responsible staff.
- Track ticket status from open to resolved.
- Maintain follow-up notes on eligible tickets.
- Display an ordered queue of unresolved work.
- Generate reports on ticket totals, statuses, and priorities.
- Persist ticket records using JSON.
- Use automated tests to improve reliability and maintainability.

## 3. Team Members and Responsibilities

### Engineer A: Blessing Anebi

**Focus: Ticket creation and priority calculation**

Responsibilities include:
- Creating and validating tickets.
- Generating ticket IDs.
- Calculating ticket priority.
- Writing and maintaining relevant automated tests.

### Engineer B: Philip Edward

**Focus: Workflow and data management**

Responsibilities include:
- Managing ticket assignment and status transitions.
- Supporting JSON persistence.
- Working on workflow and data-management tests.
- Helping integrate and verify the application.

Both engineers contribute to testing, documentation, code review, and integration.

## 4. Tools and Technologies

- **Python 3:** Application development.
- **Git:** Version control.
- **GitHub:** Collaboration and pull-request reviews.
- **unittest:** Automated testing.
- **JSON:** Ticket data persistence.

The project uses Python's standard library for its core functionality.

## 5. Features

The application includes the following functionality:

- Ticket creation with a title, category, urgency, and number of affected users.
- Automatic ticket ID generation, such as `T001`.
- Automatic priority calculation.
- Input validation.
- Ticket listing and individual ticket viewing.
- Staff assignment.
- Status updates with workflow rules.
- A work queue ordered by priority and ticket ID.
- Reports showing ticket totals, statuses, and priorities.
- Follow-up notes for eligible tickets.
- JSON-based saving and loading of ticket records.

Search and combined-filter functionality should be confirmed against the latest integrated code before being described as completed features.

## 6. Setup

### Requirements

You need:
- Python 3.
- Git.
- A terminal or code editor, such as Visual Studio Code.

### Clone the repository

```bash
git clone https://github.com/Oanebi/CampusFlow.git
cd CampusFlow
```

### Create a virtual environment

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

No third-party packages are currently required for the core application.

## 7. Running the Application

From the project root, run:

```bash
python3 main.py
```

The command-line menu provides options to:

1. Create a ticket.
2. List tickets.
3. View a ticket.
4. Assign a ticket.
5. Update ticket status.
6. View the work queue.
7. View reports.
8. Exit.

Follow the prompts displayed by the application.

## 8. Ticket Priority

Priority is calculated from the urgency of the problem and the number of affected users.

| Condition | Priority |
|---|---|
| High urgency and at least 10 affected users | Critical |
| High urgency or at least 10 affected users, unless critical applies | High |
| Medium urgency or at least 3 affected users, unless a higher priority applies | Medium |
| All other valid combinations | Low |

Accepted urgency values are `low`, `medium`, and `high`.

For example, a high-urgency problem affecting 15 users receives critical priority.

## 9. Ticket Workflow

A newly created ticket starts with status `open` and no assigned staff member.

The workflow supports these statuses:

- `open`
- `in_progress`
- `resolved`

A ticket must be assigned before it can move from `open` to `in_progress`. An in-progress ticket can be resolved. A resolved ticket must be explicitly reopened before further modification.

These rules help prevent invalid status changes and accidental updates to resolved tickets.

## 10. Follow-up Notes

Tickets can contain follow-up notes recording additional information about a problem.

Each note includes:
- A note ID, such as `N001`.
- The author's name.
- A message.

Notes are limited to eligible tickets, and their author and message are validated. Note IDs are generated independently for each ticket.

## 11. Work Queue and Reports

The work queue displays open tickets in priority order:

1. Critical
2. High
3. Medium
4. Low

Tickets with the same priority are ordered by numeric ticket ID.

The reports functionality summarizes ticket totals, ticket statuses, and priority counts. Reports should also handle the case where no tickets exist.

## 12. JSON Storage

CampusFlow Next uses JSON to persist ticket data.

The default storage path is:

`data/tickets.json`

The storage module provides functions to save and load ticket records. A missing data file starts with an empty ticket list, while invalid JSON or invalid ticket data should produce a clear error.

Ticket records can include follow-up notes. The application should be tested to confirm that tickets and their notes survive a save-and-reload cycle.

The JSON file contains application data, not Python source code.

## 13. Running the Tests

CampusFlow Next uses Python's built-in `unittest` framework.

Run the complete test suite from the project root:

```bash
python3 -m unittest discover -s tests -v
```

To run an individual test file:

```bash
python3 -m unittest discover -s tests -p "test_tickets.py" -v
```

The tests cover ticket creation, priority calculation, workflow rules, reports, storage, and notes.

During development, the full suite passed **67 tests**. Re-run it against the latest integrated `main` branch before submitting the project, and update this result if the test count or outcome changes.

## 14. Project Structure

The project includes the following main files:

```text
CampusFlow/
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── workflow.py
│   ├── storage.py
│   ├── reports.py
│   └── notes.py
├── tests/
│   ├── test_tickets.py
│   ├── test_workflow.py
│   ├── test_storage.py
│   ├── test_reports.py
│   └── test_notes.py
├── docs/
│   ├── baseline-check.md
│   ├── design-decisions.md
│   └── ai-learning-log.md
├── data/
├── main.py
├── README.md
└── .gitignore
```

This describes the intended project layout. Confirm the actual files in the repository before treating the tree as exhaustive.

## 15. Known Limitations and Verification

Before final submission, the team must verify:

- Search and combined filters, if required by the final specification.
- Correct behavior when invalid data is supplied.
- Safe handling of failed saves and malformed JSON.
- Correct save-and-reload behavior for tickets and notes.
- The complete CLI demonstration on the latest integrated `main` branch.

Any unresolved failures or incomplete features must be documented honestly.

## 16. GitHub Workflow

The team uses feature branches and pull requests to review changes before merging them into `main`.

The normal workflow is:

1. Update the local `main` branch.
2. Create a feature branch.
3. Implement the change and add tests.
4. Run the relevant tests and full test suite.
5. Commit and push the branch.
6. Open a pull request.
7. Request and complete peer review.
8. Merge after required approval.

Example:

```bash
git switch main
git pull origin main
git switch -c feature/your-feature
```

After making changes:

```bash
git add path/to/changed-files
git commit -m "feat: describe your change"
git push -u origin feature/your-feature
```

Feature work should not be committed directly to `main`. Each engineer should review the other engineer's pull request and address blocking feedback before merging.

## 17. Project Documentation and Learning Evidence

The `docs/` directory records the project's development and engineering decisions.

- `baseline-check.md` documents the initial application state, environment, commands, representative inputs, and observed results.
- `design-decisions.md` records function contracts, data structures, validation rules, and module responsibilities.
- `ai-learning-log.md` records genuine learning questions, experiments, independent verification, results, and critical evaluations of AI suggestions.

These documents should reflect actual work performed by both engineers.

## 18. Final Verification and Submission

Before submission, the team will:

- Run the full test suite on the latest integrated `main` branch.
- Demonstrate the required ticket creation, workflow, queue, reports, notes, search, and persistence behavior.
- Confirm both engineers' contributions and pull-request reviews.
- Record the repository URL, pull-request links, test results, both engineers' names, and final `main` commit SHA.

CampusFlow Next aims to make campus helpdesk work more organized, traceable, and testable through a simple Python application.