"""Tests for the part of scripts/lint_content.py that decides whether every example file is used."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import lint_content  # noqa: E402


@pytest.fixture
def examples(tmp_path, monkeypatch):
    """A temporary stand-in for the repository, with lint_content pointed at it."""
    monkeypatch.setattr(lint_content, "REPO", tmp_path)
    monkeypatch.setattr(lint_content, "EXAMPLES", tmp_path / "examples")

    def write(files: list[str]) -> None:
        for name in files:
            path = tmp_path / "examples" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("")

    return write


def problems_for(used: set[str]) -> list[str]:
    return [str(problem) for problem in lint_content.lint_examples_used({"ch01/page.md": used}, final=False)]


def test_every_file_of_a_project_must_be_included_by_a_page(examples):
    examples(["ch01/02-add/main.cpp", "ch01/02-add/add.cpp", "ch01/02-add/add.h", "ch01/02-add.out"])
    used = {"examples/ch01/02-add/main.cpp", "examples/ch01/02-add/add.cpp", "examples/ch01/02-add.out"}
    problems = problems_for(used)
    assert len(problems) == 1 and "add.h" in problems[0] and "is not used by any page" in problems[0]


def test_a_fully_included_project_has_no_problems(examples):
    files = ["ch01/02-add/main.cpp", "ch01/02-add/add.h", "ch01/02-add.out"]
    examples(files)
    assert problems_for({f"examples/{name}" for name in files}) == []


def test_an_input_file_may_belong_to_a_project_folder_next_to_it(examples):
    examples(["ch01/02-add/main.cpp", "ch01/02-add.in"])
    assert problems_for({"examples/ch01/02-add/main.cpp"}) == []


def test_an_input_file_may_belong_to_a_single_file_program(examples):
    examples(["ch01/01-read.cpp", "ch01/01-read.in"])
    assert problems_for({"examples/ch01/01-read.cpp"}) == []


def test_an_input_file_without_a_program_is_reported(examples):
    examples(["ch01/01-a.cpp", "ch01/09-orphan.in"])
    problems = problems_for({"examples/ch01/01-a.cpp"})
    assert len(problems) == 1 and "09-orphan.in" in problems[0] and "no program" in problems[0]


def test_files_the_operating_system_adds_are_not_examples(examples):
    examples(["ch01/01-a.cpp", "ch01/.DS_Store"])
    assert problems_for({"examples/ch01/01-a.cpp"}) == []
