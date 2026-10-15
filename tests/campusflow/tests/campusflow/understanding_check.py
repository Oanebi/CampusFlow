"""Engineering Understanding Check for CampusFlow Next."""

QUESTIONS = [
    {
        "question": (
            "T001 is open and unassigned. Someone tries to move it "
            "to in_progress. What should happen?"
        ),
        "options": {
            "A": "Accept the change",
            "B": "Reject and preserve all data",
            "C": "Resolve it automatically",
            "D": "Remove the ticket",
        },
        "answer": "B",
    },
    {
        "question": (
            "The application has zero tickets. What is the "
            "resolution percentage?"
        ),
        "options": {
            "A": "Crash",
            "B": "100%",
            "C": "0%",
            "D": "Divide by one without explanation",
        },
        "answer": "C",
    },
    {
        "question": (
            "A search uses title='wifi', category='Network', "
            "and status='open'. Which tickets should match?"
        ),
        "options": {
            "A": "Tickets matching any one filter",
            "B": "Tickets matching all supplied filters",
            "C": "All Network tickets",
            "D": "All open tickets",
        },
        "answer": "B",
    },
    {
        "question": (
            "A resolved ticket receives an Add Follow-up Note request. "
            "What should happen?"
        ),
        "options": {
            "A": "Append the note anyway",
            "B": "Delete old notes",
            "C": "Reject until the ticket is reopened",
            "D": "Change the status silently",
        },
        "answer": "C",
    },
    {
        "question": (
            "The JSON file contains two tickets with the same ID. "
            "What should loading do?"
        ),
        "options": {
            "A": "Keep both tickets",
            "B": "Replace memory with duplicates",
            "C": "Reject the load without changing current memory",
            "D": "Rename the IDs silently",
        },
        "answer": "C",
    },
    {
        "question": (
            "A pull request changes validation but contains no negative "
            "tests. What is the best review action?"
        ),
        "options": {
            "A": "Approve because it runs",
            "B": "Request focused tests and reasoning",
            "C": "Merge immediately",
            "D": "Ask AI to approve it",
        },
        "answer": "B",
    },
]


def score_answers(answers):
    """Return the number of correct answers, from zero to six."""

    score = 0

    for question, answer in zip(QUESTIONS, answers):
        if isinstance(answer, str):
            if answer.strip().upper() == question["answer"]:
                score += 1

    return score


def get_valid_answer(question, input_fn=input, output_fn=print):
    """Keep asking until the user enters A, B, C, or D."""

    valid_options = {"A", "B", "C", "D"}

    while True:
        answer = input_fn(
            f"{question['question']}\n"
            "Choose A, B, C, or D: "
        ).strip().upper()

        if answer in valid_options:
            return answer

        output_fn("Invalid choice. Please enter A, B, C, or D.")


def run_understanding_check(input_fn=input, output_fn=print):
    """Run the quiz and collect two short explanations."""

    answers = []

    output_fn("\n=== Engineering Understanding Check ===")

    for number, question in enumerate(QUESTIONS, start=1):
        output_fn(f"\nQuestion {number}:")

        for option, text in question["options"].items():
            output_fn(f"  {option}. {text}")

        answer = get_valid_answer(
            question,
            input_fn=input_fn,
            output_fn=output_fn,
        )

        answers.append(answer)

        if answer == question["answer"]:
            output_fn("Answer recorded.")
        else:
            output_fn("Answer recorded.")

    score = score_answers(answers)

    output_fn(f"\nFinal score: {score}/{len(QUESTIONS)}")

    explanations = []

    for number in (1, 2):
        while True:
            explanation = input_fn(
                f"Explain why your answer to question {number} "
                "is correct: "
            ).strip()

            if explanation:
                explanations.append(
                    {
                        "question": number,
                        "answer": answers[number - 1],
                        "explanation": explanation,
                    }
                )
                break

            output_fn("Please provide a short explanation.")

    output_fn(
        "Your explanations have been collected for discussion "
        "with your mentor."
    )

    return {
        "answers": answers,
        "score": score,
        "explanations": explanations,
    }