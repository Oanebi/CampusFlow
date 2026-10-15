"""Engineering understanding check for CampusFlow."""


QUESTIONS = [
    {
        "question": "What should happen before an unassigned ticket "
                    "moves to in_progress?",
        "options": {
            "A": "Delete the ticket",
            "B": "Assign the ticket",
            "C": "Generate a report",
            "D": "Add a note",
        },
        "answer": "B",
    },
    {
        "question": "What should the resolution percentage be when "
                    "there are no tickets?",
        "options": {
            "A": "100%",
            "B": "Undefined",
            "C": "0%",
            "D": "50%",
        },
        "answer": "C",
    },
    {
        "question": "When several search filters are supplied, "
                    "how should they work?",
        "options": {
            "A": "Only the first filter applies",
            "B": "A ticket must match every supplied filter",
            "C": "Filters are ignored",
            "D": "Only the last filter applies",
        },
        "answer": "B",
    },
    {
        "question": "Which string method supports case-insensitive "
                    "comparisons?",
        "options": {
            "A": "casefold()",
            "B": "split()",
            "C": "strip()",
            "D": "isdigit()",
        },
        "answer": "A",
    },
    {
        "question": "Why should invalid notes be rejected before "
                    "changing ticket data?",
        "options": {
            "A": "To make the program slower",
            "B": "To protect data integrity",
            "C": "To delete old notes",
            "D": "To change ticket priorities",
        },
        "answer": "B",
    },
    {
        "question": "What should a ticket search do to the original "
                    "ticket records?",
        "options": {
            "A": "Delete unmatched tickets",
            "B": "Change their priorities",
            "C": "Leave them unchanged",
            "D": "Change their statuses",
        },
        "answer": "C",
    },
]


def get_valid_answer(input_fn=input, output_fn=print):
    """Request a valid multiple-choice answer."""

    while True:
        answer = input_fn("Your answer (A/B/C/D): ").strip().upper()

        if answer in {"A", "B", "C", "D"}:
            return answer

        output_fn("Invalid answer. Please enter A, B, C, or D.")


def score_answers(answers):
    """Calculate the number of correct answers."""

    if len(answers) != len(QUESTIONS):
        raise ValueError(
            f"Expected {len(QUESTIONS)} answers."
        )

    return sum(
        answer.strip().upper() == question["answer"]
        for answer, question in zip(answers, QUESTIONS)
    )


def run_quiz(input_fn=input, output_fn=print):
    """Run the engineering understanding quiz."""

    answers = []

    output_fn("\n--- Engineering Understanding Check ---")

    for number, question in enumerate(QUESTIONS, start=1):
        output_fn(f"\nQuestion {number}: {question['question']}")

        for option, text in question["options"].items():
            output_fn(f"{option}. {text}")

        answers.append(get_valid_answer(input_fn, output_fn))

    score = score_answers(answers)

    output_fn(f"\nYour score: {score}/{len(QUESTIONS)}")
    output_fn("Understanding check completed.")

    return score