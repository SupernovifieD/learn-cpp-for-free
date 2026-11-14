"""Tests for prove_session in scripts/check_examples.py: is X.session the program's output with the typed lines mixed in?

These tests need no compiler. The tests in test_check_examples.py run the whole checker on sessions.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_examples  # noqa: E402


def prove(session: str, typed: str, stdout: str) -> str | None:
    return check_examples.prove_session(session.encode(), typed.encode(), stdout.encode())


def test_a_session_is_the_output_with_the_typed_line_where_the_reader_typed_it():
    assert prove("Enter a number: 7\nTwice that is 14\n", "7\n", "Enter a number: Twice that is 14\n") is None


def test_several_typed_lines_are_each_placed_after_their_prompt():
    session = "Width: 3\nHeight: 4\nArea: 12\n"
    assert prove(session, "3\n4\n", "Width: Height: Area: 12\n") is None


def test_a_program_that_reads_nothing_has_the_session_equal_to_its_output():
    assert prove("Hello\n", "", "Hello\n") is None


def test_a_typed_line_that_looks_like_earlier_output_is_still_found():
    # The program prints "n=1", asks "q: ", the reader types 1, and the program prints "r".
    # The first "1\n" in the session belongs to the output, so deleting the first match is wrong.
    assert prove("n=1\nq: 1\nr\n", "1\n", "n=1\nq: r\n") is None


def test_two_identical_typed_lines_are_both_found():
    assert prove("go: 5\ngo: 5\nbye\n", "5\n5\n", "go: go: bye\n") is None


def test_a_wrong_output_line_names_the_line_and_what_the_program_prints():
    message = prove("Enter a number: 7\nTwice that is 15\n", "7\n", "Enter a number: Twice that is 14\n")
    assert message is not None
    assert "line 2 of X.session" in message and "Twice that is 15" in message
    assert "Twice that is 14" in message


def test_a_session_without_the_typed_line_names_the_missing_line():
    message = prove("Enter a number: \nTwice that is 14\n", "7\n", "Enter a number: Twice that is 14\n")
    assert message is not None
    assert "line 1 of X.session reads 'Enter a number: '" in message
    assert "the reader types '7' (typed line 1 of X.in)" in message


def test_an_input_line_that_the_session_never_shows_is_reported():
    message = prove("Enter a number: 7\nTwice that is 14\n", "7\n9\n", "Enter a number: Twice that is 14\n")
    assert message is not None
    assert "typed line 2 of X.in ('9') does not appear in X.session" in message


def test_a_session_that_stops_before_the_program_does_is_reported():
    message = prove("Enter a number: 7\n", "7\n", "Enter a number: Twice that is 14\n")
    assert message is not None
    assert "ends too early" in message and "Twice that is 14" in message


def test_text_in_the_session_after_everything_is_reported():
    message = prove("Hello\nGoodbye\n", "", "Hello\n")
    assert message is not None
    assert "line 2 of X.session" in message and "nothing more is printed or typed" in message


def test_the_names_of_the_files_appear_in_messages():
    message = check_examples.prove_session(b"x\n", b"1\n", b"x\n", ("02-sum.in", "02-sum.session"))
    assert message is not None and "02-sum.in" in message and "02-sum.session" in message


def test_a_long_session_is_proved_quickly():
    # 2,000 prompts. The proof is not linear in the worst case, but a realistic session must stay quick.
    count = 2000
    stdout = "q: \n" * count
    typed = "1\n" * count
    session = "q: 1\n\n" * count
    started = time.perf_counter()
    assert check_examples.prove_session(session.encode(), typed.encode(), stdout.encode()) is None
    assert time.perf_counter() - started < 20, "proving a 2,000-prompt session took far too long"


def test_the_proof_checks_the_order_of_the_typed_lines_but_not_where_they_sit():
    # Documented limits (CONTRIBUTING.md): a typed line before its prompt, or after all the output, is accepted.
    # The author must place the lines as the program would show them.
    assert prove("7\nEnter a number: Twice that is 14\n", "7\n", "Enter a number: Twice that is 14\n") is None
    assert prove("Enter a number: Twice that is 14\n7\n", "7\n", "Enter a number: Twice that is 14\n") is None
    # But two typed lines in the wrong order are caught.
    assert prove("a: 2\nb: 1\n", "1\n2\n", "a: b: \n") is not None
