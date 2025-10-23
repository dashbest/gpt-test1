"""Unit tests for the children's quiz app."""
from __future__ import annotations

import builtins
import pathlib
import sys
from typing import Iterable
from unittest import mock

# Ensure the project root is on ``sys.path`` so ``quiz_app`` can be imported when
# pytest executes from the ``tests`` directory.
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import quiz_app


def _make_question(prompt: str, answer: str, choices: Iterable[str]):
    return quiz_app.Question(prompt=prompt, answer=answer, hint="hint", choices=tuple(choices))


def test_build_quiz_randomizes_order():
    questions = [
        _make_question("Q1", "A", ["A", "B", "C"]),
        _make_question("Q2", "B", ["A", "B", "C"]),
        _make_question("Q3", "C", ["A", "B", "C"]),
    ]

    first_run = quiz_app.build_quiz(questions)
    second_run = quiz_app.build_quiz(questions)

    assert sorted(first_run, key=lambda q: q.prompt) == sorted(second_run, key=lambda q: q.prompt)
    # While shuffling can, in theory, produce the same order, reseeding to a fixed
    # state allows us to check that the function calls ``random.shuffle``.
    with mock.patch("quiz_app.random.shuffle") as shuffle_mock:
        quiz_app.build_quiz(questions)
        shuffle_mock.assert_called_once()


def test_ask_question_positive_path(monkeypatch):
    question = _make_question("What is 2 + 2?", "4", ["3", "4", "5"])

    inputs = iter(["2"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    with mock.patch("quiz_app.random.choice", return_value="Great job!"):
        assert quiz_app.ask_question(question) is True


def test_ask_question_handles_retry(monkeypatch):
    question = _make_question("What color is grass?", "Green", ["Blue", "Green", "Red"])

    inputs = iter(["1", "2"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    with mock.patch("quiz_app.random.choice", side_effect=["No worries", "Great job!"]):
        assert quiz_app.ask_question(question) is True


def test_ask_question_fails_after_two_attempts(monkeypatch):
    question = _make_question("What color is the sun?", "Yellow", ["Blue", "Pink", "Purple"])

    inputs = iter(["1", "3"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    with mock.patch("quiz_app.random.choice", return_value="Nice try"):
        assert quiz_app.ask_question(question) is False
