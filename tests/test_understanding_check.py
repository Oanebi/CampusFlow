import unittest
from unittest.mock import Mock

from campusflow.understanding_check import (
    QUESTIONS,
    get_valid_answer,
    run_quiz,
    score_answers,
)


class TestUnderstandingCheck(unittest.TestCase):

    def test_quiz_has_six_questions(self):
        self.assertEqual(len(QUESTIONS), 6)

    def test_score_all_correct_answers(self):
        answers = [
            question["answer"]
            for question in QUESTIONS
        ]

        self.assertEqual(score_answers(answers), 6)

    def test_score_all_incorrect_answers(self):
        answers = [
            "Z" if question["answer"] != "Z" else "Y"
            for question in QUESTIONS
        ]

        self.assertEqual(score_answers(answers), 0)

    def test_score_partially_correct_answers(self):
        answers = [
            question["answer"]
            for question in QUESTIONS
        ]
        answers[0] = (
            "A" if answers[0] != "A" else "B"
        )

        self.assertEqual(score_answers(answers), 5)

    def test_invalid_answer_is_rejected(self):
        input_fn = Mock(side_effect=["X", "A"])
        output_fn = Mock()

        answer = get_valid_answer(
            input_fn=input_fn,
            output_fn=output_fn,
        )

        self.assertEqual(answer, "A")
        self.assertEqual(input_fn.call_count, 2)
        output_fn.assert_called_once()

    def test_score_rejects_wrong_number_of_answers(self):
        with self.assertRaises(ValueError):
            score_answers(["A", "B"])

    def test_run_quiz_returns_score(self):
        answers = [
            question["answer"]
            for question in QUESTIONS
        ]

        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        score = run_quiz(
            input_fn=input_fn,
            output_fn=output_fn,
        )

        self.assertEqual(score, 6)
        self.assertEqual(input_fn.call_count, 6)

        displayed_text = "\n".join(
            str(call.args[0])
            for call in output_fn.call_args_list
        )

        self.assertIn("Your score: 6/6", displayed_text)


if __name__ == "__main__":
    unittest.main()
