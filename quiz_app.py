"""Friendly quiz app for young children.

This module contains simple functions for running a multiple-choice quiz
geared toward five-year-old children.  The quiz uses a small bank of
questions with bright, positive feedback messages.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class Question:
    """Simple representation of a quiz question.

    Attributes:
        prompt: The question to ask the player.
        choices: Possible answers displayed to the player.
        answer: The correct answer from the choices list.
        hint: A short hint to encourage the player.
    """

    prompt: str
    choices: Sequence[str]
    answer: str
    hint: str


POSITIVE_FEEDBACK = [
    "Great job!",
    "You are a star!",
    "Fantastic!",
    "Wow, super smart!",
]

GENTLE_RETRY = [
    "Nice try, let's think again!",
    "Almost! Listen to the hint.",
    "No worries, you can do it!",
]


def _default_questions() -> List[Question]:
    """Return the default bank of questions for the quiz."""

    return [
        Question(
            prompt="What color is the sky on a sunny day?",
            choices=("Blue", "Green", "Purple"),
            answer="Blue",
            hint="Look up during the day!",
        ),
        Question(
            prompt="Which animal says 'meow'?",
            choices=("Dog", "Cat", "Cow"),
            answer="Cat",
            hint="It purrs and likes to chase yarn!",
        ),
        Question(
            prompt="What number comes after 4?",
            choices=("3", "5", "2"),
            answer="5",
            hint="Count: 1, 2, 3, 4, ...",
        ),
        Question(
            prompt="Which fruit is yellow and curved?",
            choices=("Banana", "Apple", "Grape"),
            answer="Banana",
            hint="Monkeys love this fruit!",
        ),
        Question(
            prompt="How many wheels does a bicycle have?",
            choices=("Two", "Three", "Four"),
            answer="Two",
            hint="Count the wheels when you ride!",
        ),
    ]


def build_quiz(question_bank: Iterable[Question] | None = None) -> List[Question]:
    """Create an ordered list of questions for the quiz.

    The quiz shuffles the question bank each time so the player receives a
    slightly different experience on every run.
    """

    questions = list(question_bank if question_bank is not None else _default_questions())
    random.shuffle(questions)
    return questions


def ask_question(question: Question) -> bool:
    """Interactively prompt the user with a question.

    Returns ``True`` if the user eventually answers correctly, otherwise
    ``False``.  The question will continue to prompt until a valid option is
    selected, giving up to two attempts.
    """

    print(question.prompt)
    for index, choice in enumerate(question.choices, start=1):
        print(f"  {index}. {choice}")

    attempts = 0
    while attempts < 2:
        attempts += 1
        user_input = input("Choose the best answer (1-3): ").strip()
        if user_input.isdigit():
            idx = int(user_input) - 1
            if 0 <= idx < len(question.choices):
                picked = question.choices[idx]
                if picked == question.answer:
                    print(random.choice(POSITIVE_FEEDBACK))
                    return True
                print(random.choice(GENTLE_RETRY))
                print(f"Hint: {question.hint}")
                continue
        print("Let's try again. Remember to pick a number from the list!")

    print(f"The answer was: {question.answer}. Great effort!")
    return False


def run_quiz(question_bank: Iterable[Question] | None = None) -> None:
    """Run the full quiz, tracking and reporting the player's score."""

    score = 0
    questions = build_quiz(question_bank)
    total = len(questions)

    print("Hello, little explorer! Let's play a quiz together!\n")

    for question in questions:
        if ask_question(question):
            score += 1
        print()  # Blank line between questions

    print("All done! Here's how you did:")
    print(f"You answered {score} out of {total} questions correctly!")
    if score == total:
        print("Perfect score! You're amazing!")
    elif score >= total / 2:
        print("Great work! You're learning so fast!")
    else:
        print("Nice try! Let's play again soon and learn even more!")


if __name__ == "__main__":
    run_quiz()
