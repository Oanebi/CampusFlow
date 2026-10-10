# CampusFlow

## 1. Project Overview

CampusFlow is a Python command-line campus helpdesk ticket management system designed to help students and staff report technical problems and enable appropriate personnel to manage and resolve them.

## 2. Project Objectives

- Provide a structured way to report campus problems.
- Automatically calculate ticket priority.
- Generate ticket IDs.
- Enable staff assignment and ticket status tracking.
- Store ticket records in JSON format.

## 3. Key Features

### Ticket Creation
- Create tickets with a title and category.
- Record urgency and the number of affected users.
- Validate user inputs.
- Generate sequential ticket IDs.

### Priority Calculation
- Calculate ticket priority based on urgency and affected users.
- Categorise tickets as low, medium, high, or critical.

### Ticket Workflow
- Assign tickets to staff members.
- Update ticket status.
- Track progress towards resolution.

### Data Persistence
- Save ticket records to a JSON file.
- Load saved records when the application starts.

## 4. Technology Stack

- Python 3
- Git and GitHub
- JSON for data persistence
- Python unittest for automated testing

## 5. Team Responsibilities

### Engineer A: Ticket Creation and Priority Calculation
- Implement ticket creation.
- Calculate ticket priorities.
- Validate ticket inputs.
- Generate ticket IDs.
- Write and maintain ticket creation tests.

### Engineer B: Ticket Workflow and Data Persistence
- Implement ticket workflow management.
- Manage staff assignment and ticket status.
- Implement JSON storage.
- Save and load ticket records.
- Write and maintain workflow tests.

## 6. Running Tests

Run the automated tests with:

```bash
python3 -m unittest discover -s tests -v
```

## 7. Development Workflow

Each engineer works on a separate feature branch, tests their contribution, and submits a pull request for review and integration into the main branch.

## 8. Current Limitations

The complete application depends on integrating the ticket creation, workflow, and storage modules. Features should be considered complete only after implementation and testing.

## 9. Contributors

- Engineer A: Ticket creation and priority calculation.
- Engineer B: Ticket workflow and JSON data persistence.
