# CampusFlow – Campus Helpdesk Ticket Management System

## 1. About the Project

CampusFlow is a Python project designed to help students and staff report problems on campus and make it easier for the right people to solve them.

For example, a student may report a faulty computer in a laboratory, a network problem, or an electrical fault. CampusFlow is designed to record the problem as a ticket, calculate its priority, and help the responsible staff manage it until it is resolved.

### The Problem We Want to Solve

Sometimes, campus problems are reported verbally or through informal messages. This can make it difficult to keep records, identify urgent problems, and know which issues have been resolved.

We are building CampusFlow to provide a more organized way to report and manage these problems.

## 2. Project Objectives

The main objectives of CampusFlow are to:

- Make it easier to record problems on campus.
- Give every ticket an ID for easy identification.
- Calculate ticket priority automatically.
- Allow tickets to be assigned to staff.
- Track the progress of reported problems.
- Save ticket information for future reference.
- Make it easier to test and maintain the application.

## 3. Team Members and Responsibilities

We are working together on CampusFlow, with each team member responsible for a different part of the project.

### Engineer A: Okoh Abah
**Role: Ticket Creation and Priority Calculation**

Responsibilities:
- Creating new tickets.
- Checking that the required information is valid.
- Generating ticket IDs.
- Calculating ticket priority based on urgency and the number of affected users.
- Writing automated tests for the ticket-creation functions.

### Engineer B: Blessing Anebi
**Role: Ticket Workflow and Data Management**

Responsibilities:
- Managing ticket assignment.
- Updating ticket status.
- Working on saving and loading ticket records using JSON.
- Testing the workflow and data-management functions.

The two engineers will work together to connect their modules and test the complete application.

## 4. Tools and Technologies

We are using the following tools to build CampusFlow:

- **Python 3.12:** For writing the application.
- **Git:** For tracking changes to our code.
- **GitHub:** For sharing code and reviewing contributions.
- **Python unittest:** For testing our functions.
- **JSON:** The planned format for saving ticket records.

## 5. Features

The ticket-creation part of CampusFlow currently supports:

- Creating a ticket with a title, category, urgency, and number of affected users.
- Generating ticket IDs such as `T001` and `T002`.
- Calculating ticket priority automatically.
- Rejecting invalid ticket information.
- Setting the initial ticket status to `open`.
- Leaving the ticket unassigned until a staff member is assigned.

The wider project is also intended to support ticket assignment, status updates, and data storage. These features must be integrated and tested before we can consider the complete application ready.

## 6. How to Set Up the Project

### Requirements

You need:
- Python 3.12 or a compatible Python 3 version.
- Git.
- A terminal or an editor such as Visual Studio Code.

### Step 1: Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/Oanebi/CampusFlow.git
cd CampusFlow
```

### Step 2: Create a Virtual Environment

On Linux or macOS, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, run:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

A virtual environment helps keep the project's Python environment separate from other projects on your computer.

## 7. Running the Application

The ticket-creation functions are in:

`campusflow/tickets.py`

The current ticket-creation module provides functions for creating tickets and calculating their priorities.

The command for launching the complete interactive application and its menu options should be added after the CLI has been integrated and tested.

The completed application is expected to let users create tickets, assign staff, update ticket status, and manage reported problems.

## 8. How Ticket Priority Works

CampusFlow calculates priority using two things:

1. The urgency of the problem.
2. The number of people affected.

The current rules are:

| Condition | Priority |
|---|---|
| High urgency and 10 or more affected users | Critical |
| High urgency or 10 or more affected users, when the critical rule does not apply | High |
| Medium urgency or 3 or more affected users, when no higher rule applies | Medium |
| All other valid cases | Low |

The accepted urgency values are `low`, `medium`, and `high`.

For example, a high-urgency problem affecting 15 people receives a critical priority.

These rules help the system identify problems that may need more urgent attention.

## 9. Ticket Status

When a ticket is created, its initial status is `open`.

This means the problem has been reported and is waiting for further action.

A new ticket also starts with no assigned staff member.

The workflow part of the project is intended to manage assignments and status changes as work progresses. The final status rules will be documented after the workflow has been integrated and tested.

## 10. Running the Tests

We use Python's built-in `unittest` framework to check that our functions work as expected.

The ticket-creation tests are in:

`tests/test_tickets.py`

They check:
- Ticket priority calculation.
- Ticket creation.
- Ticket ID generation.
- Invalid urgency values.
- Invalid numbers of affected users.
- Empty or invalid titles and categories.
- Other invalid input.

To run the tests, open a terminal in the project folder and enter:

```bash
python3 -m unittest discover -s tests -v
```

The ticket-creation module currently has **17 automated tests**, and all 17 passed after the changes were merged into the `main` branch.

Tests for the workflow, JSON storage, and the complete ticket process should also be run when those parts are integrated.

## 11. Saving Ticket Information

We plan to use JSON to save ticket information because it is easy to read and Python supports it.

The current ticket-creation function returns a Python dictionary. It does not save tickets to a file by itself.

The team still needs to verify the final storage filename and location after the JSON functionality has been integrated.

Once storage is available, this section should explain how to save tickets, load existing tickets, and start with an empty set of records when needed.

## 12. Project Structure

The main files in the merged ticket-creation contribution are:

```text
CampusFlow/
├── campusflow/
│   └── tickets.py
├── tests/
│   └── test_tickets.py
├── docs/
│   └── ai-learning-log.md
├── README.md
└── .gitignore
```

Other files, including workflow and data-storage components, are part of the wider project and may be added as development continues.

## 13. Current Limitations

Some parts of CampusFlow still need to be completed or verified.

These include:
- Connecting all the modules into one working application.
- Completing and testing the interactive command-line menu.
- Verifying ticket assignment and status updates.
- Implementing and testing JSON storage.
- Testing the complete process from ticket creation to resolution.

The current ticket ID generator also depends on the list of existing tickets supplied to it. The complete application must manage saved tickets correctly to avoid duplicate IDs.

We will continue working on these areas as a team.

## 14. Future Improvements

Some improvements we would like to make include:

- Completing the interactive menu.
- Connecting ticket creation with workflow management.
- Saving and loading tickets from JSON.
- Searching for tickets.
- Generating reports on ticket priorities and status.
- Improving error messages.
- Adding more tests for the complete application.

These improvements will depend on the project's requirements and the time available.

## 15. Pull Requests and Contributions

We use GitHub to share our work and review changes before merging them into the main branch.

### Engineer A: Okoh Abah

Ticket creation and priority calculation:

[View Engineer A's pull request](https://github.com/Oanebi/CampusFlow/pull/1)

### Engineer B: Blessing Anebi

To find Engineer B's contribution and review status, visit:

[View CampusFlow pull requests on GitHub](https://github.com/Oanebi/CampusFlow/pulls)

## 16. Working on the Project

Our basic development process is:

1. Update the local `main` branch.
2. Create a branch for the feature being developed.
3. Write the code and tests.
4. Run the tests.
5. Commit and push the changes.
6. Open a pull request for review.
7. Merge the changes when they are ready.

For example:

```bash
git switch main
git pull origin main
git switch -c feature/your-feature
```

After making and testing changes:

```bash
git add .
git commit -m "feat: describe your change"
git push -u origin feature/your-feature
```

The team can then open a pull request on GitHub.

## 17. Conclusion

CampusFlow is our attempt to make reporting and managing campus problems more organized.

We have completed and tested the ticket-creation part, including ticket ID generation, input validation, and automatic priority calculation. Our next step is to connect it with the workflow and storage features so that the complete application can manage tickets from the time they are reported until they are resolved.