import unittest
from unittest.mock import Mock

from campusflow.understanding_check import (
    QUESTIONS,
    get_valid_answer,
    score_answers,
)


class TestUnderstandingCheck(unittest.TestCase):

    def test_all_correct_answers_score_six(self):
        answers = [question["answer"] for question in QUESTIONS]

        self.assertEqual(score_answers(answers), 6)

    def test_all_wrong_answers_score_zero(self):
        answers = ["A"] * 6

        self.assertEqual(score_answers(answers), 0)

    def test_mixed_answers_are_scored_correctly(self):
        answers = [
            question["answer"] for question in QUESTIONS
        ]
        answers[0] = "A"

        self.assertEqual(score_answers(answers), 5)

    def test_lowercase_answers_are_accepted(self):
        answers = [
            question["answer"].lower()
            for question in QUESTIONS
        ]

        self.assertEqual(score_answers(answers), 6)

    def test_invalid_answer_prompts_again(self):
        input_fn = Mock(side_effect=["X", "B"])
        output_fn = Mock()

        answer = get_valid_answer(
            QUESTIONS[0],
            input_fn=input_fn,
            output_fn=output_fn,
        )

        self.assertEqual(answer, "B")
        self.assertEqual(input_fn.call_count, 2)
        output_fn.assert_called_once()

    def test_empty_answers_score_zero(self):
        self.assertEqual(score_answers([]), 0)


if __name__ == "__main__":
    unittest.main()