"""Tests for scripts/check_examples.py.

Most tests run the checker as a command against the small example trees in tests/scripts/fixtures/
(each folder there is a stand-in for examples/), so they test what a contributor sees. The folder
structure rules are also tested directly on trees built in a temporary directory, because they need
no compiler.

Tests that build programs skip with a reason when no compiler is installed, except in CI (the CI
environment variable is set), where a missing compiler or clang-format is itself a failure.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parents[1] / "scripts"
FIXTURES = HERE / "fixtures"
sys.path.insert(0, str(SCRIPTS))

import check_examples  # noqa: E402

COMPILERS = [compiler for compiler in check_examples.find_compilers([]).values() if compiler]
CLANG_FORMAT = check_examples.find_clang_format()

needs_compiler = pytest.mark.skipif(not COMPILERS, reason="no real g++ or clang++ was found, so the checker cannot build anything")
needs_clang_format = pytest.mark.skipif(CLANG_FORMAT is None, reason="clang-format was not found (install requirements-dev.txt)")


def run_checker(case: str, *arguments: str) -> subprocess.CompletedProcess:
    """Run the checker on the fixture tree `case`, with the fixtures' own flags file."""
    command = [sys.executable, str(SCRIPTS / "check_examples.py"), "--root", str(FIXTURES / case), "--flags-file", str(FIXTURES / "flags.txt"), *arguments]
    result = subprocess.run(command, capture_output=True, text=True, timeout=300)
    result.output = result.stdout + result.stderr  # type: ignore[attr-defined]
    return result


def make_tree(root: Path, files: dict[str, str]) -> Path:
    """Write a tree of files below root/examples and return the examples folder."""
    examples = root / "examples"
    for name, text in files.items():
        path = examples / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return examples


MINIMAL = "int main()\n{\n    return 0;\n}\n"


@pytest.mark.skipif(not os.environ.get("CI"), reason="only CI insists on the tools")
def test_ci_has_a_compiler_and_clang_format():
    assert COMPILERS, "CI must have a real g++ or clang++, or every build test would be skipped."
    assert CLANG_FORMAT, "CI must have clang-format, or every format test would be skipped."


# --------------------------------------------------------------- the whole checker --


@needs_compiler
def test_a_good_tree_with_files_projects_and_failing_programs_passes():
    run = run_checker("good")
    assert run.returncode == 0, run.output
    assert "5 of 5 examples passed." in run.output
    assert "good/ch01/02-add/" in run.output  # a project is one row, with a trailing slash
    assert "FAIL" not in run.output


@needs_compiler
def test_a_project_folder_or_a_file_in_it_selects_the_whole_project():
    root = FIXTURES / "good" / "ch01"
    for target in (root / "02-add", root / "02-add" / "add.h"):
        run = run_checker("good", str(target))
        assert run.returncode == 0, run.output
        assert "1 of 1 examples passed." in run.output


def test_an_argument_that_is_not_a_program_is_reported():
    run = run_checker("good", str(FIXTURES / "good" / "ch01" / "02-add.out"))
    assert run.returncode != 0
    assert "is not a program, a project folder or a file of a project" in run.output


@needs_compiler
def test_a_project_that_does_not_build_but_is_not_marked_failing_is_reported_with_a_fix():
    run = run_checker("unmarked-failure")
    assert run.returncode == 1, run.output
    assert "01-broken/" in run.output
    assert "use of undeclared identifier" in run.output or "was not declared" in run.output
    assert "If this program is meant to fail, rename it 01-broken.fail/" in run.output


@needs_compiler
def test_a_failing_project_that_builds_is_reported():
    run = run_checker("fail-that-builds")
    assert run.returncode == 1, run.output
    assert "01-fine.fail/" in run.output
    assert "built this program, but it is marked as failing" in run.output


@needs_compiler
@needs_clang_format
def test_a_badly_formatted_header_is_reported():
    run = run_checker("bad-header-format")
    assert run.returncode == 1, run.output
    assert "clang-format would change this program" in run.output
    assert "util.h" in run.output


@needs_compiler
def test_an_81_column_header_line_is_reported_with_its_file_and_line():
    run = run_checker("wide-header")
    assert run.returncode == 1, run.output
    assert "limit is 80: util.h: line 1 has 81 columns" in run.output


@needs_compiler
def test_a_header_outside_a_project_is_reported_with_a_fix():
    run = run_checker("header-outside-project")
    assert run.returncode == 1, run.output
    assert ".h files may only live inside a project folder" in run.output
    assert "helper.h" in run.output


@needs_compiler
def test_a_stray_out_file_is_reported():
    run = run_checker("stray-out")
    assert run.returncode == 1, run.output
    assert "02-orphan.out has no matching program" in run.output


# ------------------------------------------------- the folder rules (no compiler) --


def discover(tmp_path: Path, files: dict[str, str]):
    examples = make_tree(tmp_path, files)
    return check_examples.discover(examples)


def test_a_project_is_one_program_and_its_companions_sit_next_to_the_folder(tmp_path):
    programs, problems = discover(
        tmp_path,
        {
            "ch01/02-add/main.cpp": MINIMAL,
            "ch01/02-add/add.cpp": MINIMAL,
            "ch01/02-add/add.h": "",
            "ch01/02-add.out": "5\n",
            "ch01/02-add.in": "2\n",
            "ch01/01-single.cpp": MINIMAL,
        },
    )
    assert problems == []
    assert sorted(p.base.name for p in programs) == ["01-single.cpp", "02-add"]
    project = next(p for p in programs if p.is_project)
    assert [s.name for s in project.sources] == ["add.cpp", "main.cpp"]
    assert [h.name for h in project.headers] == ["add.h"]
    assert project.companion(".out").name == "02-add.out"


def test_a_failing_project_keeps_the_fail_in_its_companion_name(tmp_path):
    programs, _ = discover(tmp_path, {"ch01/05-link.fail/main.cpp": MINIMAL})
    assert programs[0].expects_failure
    assert programs[0].companion(".out").name == "05-link.fail.out"


@pytest.mark.parametrize(
    "files, expected",
    [
        ({"ch01/01-a/main.cpp": MINIMAL, "ch01/01-a/more/x.cpp": MINIMAL}, "is a folder inside a project"),
        ({"ch01/01-a/helper.cpp": MINIMAL}, "needs a main.cpp"),
        ({"ch01/01-a/main.cpp": MINIMAL, "ch01/01-a/notes.txt": ""}, "unexpected file type inside a project folder"),
        ({"ch01/01-a/main.cpp": MINIMAL, "ch01/01-a/01-a.out": ""}, "NEXT TO the folder"),
        ({"ch01/01-a.cpp": MINIMAL, "ch01/01-a/main.cpp": MINIMAL}, "have the same name"),
        ({"top-level.cpp": MINIMAL, "ch01/01-a.cpp": MINIMAL}, "not allowed directly in examples/"),
        ({"ch01/shared.h": ""}, ".h files may only live inside a project folder"),
        ({"ch01/01-a.cpp": MINIMAL, "ch01/01-a.txt": ""}, "unexpected file type"),
        ({"ch01/01-a.cpp": MINIMAL, "ch01/02-b.in": ""}, "02-b.in has no matching program"),
    ],
)
def test_structure_problems_say_what_is_wrong(tmp_path, files, expected):
    _, problems = discover(tmp_path, files)
    assert any(expected in problem for problem in problems), problems


def test_files_the_operating_system_adds_are_ignored(tmp_path):
    programs, problems = discover(tmp_path, {"ch01/01-a.cpp": MINIMAL, "ch01/.DS_Store": "", ".DS_Store": ""})
    assert problems == [] and len(programs) == 1


def check_rules(tmp_path: Path, files: dict[str, str]) -> list[str]:
    programs, _ = discover(tmp_path, files)
    result = check_examples.Result("x")
    for program in programs:
        check_examples.check_rules(program, result)
    return result.problems


def test_a_failing_program_must_say_why_and_never_has_companion_files(tmp_path):
    problems = check_rules(tmp_path, {"ch01/01-a.fail.cpp": MINIMAL, "ch01/01-a.fail.out": ""})
    assert any("must start the file with the line '// expect-fail" in p for p in problems), problems
    assert any("a failing program never runs" in p for p in problems), problems


def test_the_expect_fail_comment_is_for_failing_programs_only(tmp_path):
    problems = check_rules(tmp_path, {"ch01/01-a.cpp": "// expect-fail: nope\n" + MINIMAL})
    assert any("only failing programs" in p for p in problems), problems


def test_the_expect_fail_line_of_a_failing_project_goes_into_main_cpp(tmp_path):
    problems = check_rules(tmp_path, {"ch01/01-a.fail/main.cpp": MINIMAL, "ch01/01-a.fail/other.cpp": "// expect-fail: here\n" + MINIMAL})
    assert any("main.cpp of the project" in p for p in problems), problems
