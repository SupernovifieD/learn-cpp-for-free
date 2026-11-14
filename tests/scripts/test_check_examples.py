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
import tempfile
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
CLANG = next((compiler for compiler in COMPILERS if compiler.kind == "clang"), None)
needs_clang = pytest.mark.skipif(CLANG is None, reason="no real clang++ was found, which the stand-in compilers in fixtures/bin wrap")




@pytest.fixture(scope="session")
def sanitizer_compilers() -> list:
    """The compilers on this machine that can build and run programs with the sanitizers (probing is slow, so once)."""
    with tempfile.TemporaryDirectory() as tmp:
        return [compiler for compiler in COMPILERS if check_examples.probe_sanitizers(compiler, Path(tmp)) is None]


@pytest.fixture
def working_sanitizers(sanitizer_compilers) -> list:
    if not sanitizer_compilers:
        pytest.skip("no compiler here has a working sanitizer runtime")
    return sanitizer_compilers


def run_checker(case: str, *arguments: str, sanitizers: bool = False, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    """Run the checker on the fixture tree `case`, with the fixtures' own flags file.

    The sanitizer builds are slow, so they are skipped unless a test is about them.
    """
    skip = [] if sanitizers else ["--skip-sanitizers"]
    command = [sys.executable, str(SCRIPTS / "check_examples.py"), "--root", str(FIXTURES / case), "--flags-file", str(FIXTURES / "flags.txt"), *skip, *arguments]
    result = subprocess.run(command, capture_output=True, text=True, timeout=300, env={**os.environ, **(env or {})})
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
def test_ci_has_a_compiler_and_clang_format(sanitizer_compilers):
    assert COMPILERS, "CI must have a real g++ or clang++, or every build test would be skipped."
    assert CLANG_FORMAT, "CI must have clang-format, or every format test would be skipped."
    assert sanitizer_compilers, "CI must have a working AddressSanitizer and UBSan, or the sanitizer tests would be skipped."


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


# ------------------------------------------------------------ console sessions --


@needs_compiler
def test_sessions_of_files_and_projects_are_proved_against_the_input_and_the_output():
    run = run_checker("good-session")
    assert run.returncode == 0, run.output
    assert "3 of 3 examples passed." in run.output
    assert "good-session/ch01/02-sum/" in run.output


@needs_compiler
def test_a_session_with_a_wrong_output_line_is_reported():
    run = run_checker("session-wrong-output")
    assert run.returncode == 1, run.output
    assert "line 2 of 01-twice.session reads 'Twice that is 15'" in run.output
    assert "Twice that is 14" in run.output


@needs_compiler
def test_a_session_that_is_missing_a_typed_line_is_reported():
    run = run_checker("session-missing-typed-line")
    assert run.returncode == 1, run.output
    assert "the reader types '7' (typed line 1 of 01-twice.in)" in run.output


@needs_compiler
def test_an_input_line_that_the_session_never_shows_is_reported():
    run = run_checker("session-unused-input")
    assert run.returncode == 1, run.output
    assert "typed line 2 of 01-twice.in ('9') does not appear in 01-twice.session" in run.output


def test_a_program_cannot_have_both_an_out_file_and_a_session():
    run = run_checker("session-and-out")
    assert run.returncode == 1, run.output
    assert "01-twice.out and 01-twice.session cannot both exist" in run.output


def test_an_input_file_needs_a_session_instead_of_an_out_file():
    run = run_checker("session-in-without-session")
    assert run.returncode == 1, run.output
    assert "01-twice.in needs 01-twice.session" in run.output
    assert "replace 01-twice.out by 01-twice.session" in run.output


# ------------------------------------------------------------------ sanitizers --


def cells_of(output: str, name: str) -> list[str]:
    """The result cells (gcc, clang, san, 80col, format) of the table row that names `name`."""
    row = next(line for line in output.splitlines() if name in line)
    return row.split()[1:]


@needs_compiler
def test_a_running_program_is_also_run_under_the_sanitizers_and_a_failing_one_is_not(sanitizer_compilers):
    run = run_checker("good", sanitizers=True)
    assert run.returncode == 0, run.output
    assert cells_of(run.output, "01-hello.cpp")[2] == ("PASS" if sanitizer_compilers else "SKIP")
    assert cells_of(run.output, "03-never-builds.fail.cpp")[2] == "-"


def test_a_run_time_finding_fails_even_though_the_program_builds_cleanly(working_sanitizers):
    run = run_checker("sanitizer-finding", sanitizers=True)
    assert run.returncode == 1, run.output
    assert "AddressSanitizer and UBSan" in run.output
    assert "signed integer overflow" in run.output
    # The same program is fine without the sanitizer run, so the sanitizers caused the failure.
    relaxed = run_checker("sanitizer-finding")  # without the sanitizer run
    assert relaxed.returncode == 0, relaxed.output


@needs_clang
def test_a_compiler_without_a_sanitizer_runtime_only_warns_unless_everything_is_required():
    nosan = str(FIXTURES / "bin" / "clang++-nosan")
    lenient = run_checker("good", sanitizers=True, env={"CLANGXX": nosan})
    assert lenient.returncode == 0, lenient.output
    assert "WARNING clang sanitizers:" in lenient.output
    assert "sanitizer runtime is probably not installed" in lenient.output
    strict = run_checker("good", "--require-all", sanitizers=True, env={"CLANGXX": nosan})
    assert strict.returncode == 1, strict.output
    assert "--require-all: clang sanitizers:" in strict.output


@needs_clang
def test_a_sanitizer_that_crashes_at_start_up_is_told_apart_from_a_missing_runtime(tmp_path):
    compiler = check_examples.Compiler("clang", str(FIXTURES / "bin" / "clang++-crashing"), "stand-in")
    reason = check_examples.probe_sanitizers(compiler, tmp_path)
    assert reason is not None
    assert "crashes at start-up" in reason and "vm.mmap_rnd_bits=28" in reason
    missing = check_examples.Compiler("clang", str(FIXTURES / "bin" / "clang++-nosan"), "stand-in")
    assert "probably not installed" in check_examples.probe_sanitizers(missing, tmp_path)


def test_the_probe_accepts_a_compiler_whose_sanitizers_work(tmp_path, working_sanitizers):
    assert check_examples.probe_sanitizers(working_sanitizers[0], tmp_path) is None


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


def test_a_session_needs_its_input_file(tmp_path):
    problems = check_rules(tmp_path, {"ch01/01-a.cpp": MINIMAL, "ch01/01-a.session": "x\n"})
    assert any("01-a.session needs 01-a.in" in p for p in problems), problems


def test_a_failing_program_has_no_session_either(tmp_path):
    problems = check_rules(
        tmp_path,
        {"ch01/01-a.fail.cpp": "// expect-fail: x\n" + MINIMAL, "ch01/01-a.fail.in": "1\n", "ch01/01-a.fail.session": "1\n"},
    )
    assert sum("a failing program never runs" in p for p in problems) == 2, problems


@pytest.mark.parametrize("data", ["7\r\n", "7"])
def test_typed_lines_use_unix_line_endings_and_end_with_a_newline(tmp_path, data):
    problems = check_rules(tmp_path, {"ch01/01-a.cpp": MINIMAL, "ch01/01-a.in": data, "ch01/01-a.session": "7\n"})
    assert any("must use \\n line endings (no \\r) and end with a newline" in p for p in problems), problems


def test_a_program_with_a_proper_session_has_no_rule_problems(tmp_path):
    assert check_rules(tmp_path, {"ch01/01-a.cpp": MINIMAL, "ch01/01-a.in": "7\n", "ch01/01-a.session": "x: 7\n"}) == []


def test_the_expect_fail_comment_is_for_failing_programs_only(tmp_path):
    problems = check_rules(tmp_path, {"ch01/01-a.cpp": "// expect-fail: nope\n" + MINIMAL})
    assert any("only failing programs" in p for p in problems), problems


def test_the_expect_fail_line_of_a_failing_project_goes_into_main_cpp(tmp_path):
    problems = check_rules(tmp_path, {"ch01/01-a.fail/main.cpp": MINIMAL, "ch01/01-a.fail/other.cpp": "// expect-fail: here\n" + MINIMAL})
    assert any("main.cpp of the project" in p for p in problems), problems


# ------------------------------------------------------------------ run time --


@needs_compiler
def test_a_program_that_is_really_too_slow_fails_even_after_the_second_try(tmp_path):
    """The limit is not loosened: a program that exceeds it on both tries is reported."""
    source = tmp_path / "ch01" / "01-slow.cpp"
    source.parent.mkdir()
    source.write_text('#include <chrono>\n#include <thread>\nint main()\n{\n    std::this_thread::sleep_for(std::chrono::seconds(3));\n    return 0;\n}\n')
    program = check_examples.Program(source, False, (source,), ())
    compiler = COMPILERS[0]
    exe = tmp_path / "slow"
    built = check_examples.build(compiler, ["-std=c++20"], program.sources, exe, tmp_path)
    assert built.returncode == 0, built.stderr
    message = check_examples.run_and_judge(exe, program, 1, tmp_path)
    assert message is not None and "more than 1 seconds" in message
    if sys.platform == "darwin":
        assert "in both of two tries" in message  # macOS starts a timed-out program once more


@needs_compiler
def test_a_program_that_is_fast_enough_passes_the_run_time_check(tmp_path):
    source = tmp_path / "ch01" / "01-fast.cpp"
    source.parent.mkdir()
    source.write_text("int main()\n{\n    return 0;\n}\n")
    program = check_examples.Program(source, False, (source,), ())
    exe = tmp_path / "fast"
    assert check_examples.build(COMPILERS[0], ["-std=c++20"], program.sources, exe, tmp_path).returncode == 0
    assert check_examples.run_and_judge(exe, program, 5, tmp_path) is None


@needs_compiler
@pytest.mark.skipif(sys.platform != "darwin", reason="only macOS starts a timed-out program a second time")
def test_a_program_that_is_slow_only_on_its_first_start_passes(tmp_path):
    """The first start of a new program can be slow on macOS: the second try is the one that counts."""
    marker = tmp_path / "started-before"
    source = tmp_path / "ch01" / "01-slow-once.cpp"
    source.parent.mkdir()
    source.write_text(
        '#include <chrono>\n#include <filesystem>\n#include <fstream>\n#include <thread>\nint main()\n{\n'
        f'    if (!std::filesystem::exists("{marker.name}"))\n    {{\n        std::ofstream("{marker.name}");\n'
        "        std::this_thread::sleep_for(std::chrono::seconds(3));\n    }\n    return 0;\n}\n"
    )
    program = check_examples.Program(source, False, (source,), ())
    exe = tmp_path / "slow-once"
    assert check_examples.build(COMPILERS[0], ["-std=c++20"], program.sources, exe, tmp_path).returncode == 0
    assert check_examples.run_and_judge(exe, program, 1, tmp_path) is None


# ---------------------------------------------------- messages and command line --


def test_passes_without_must_name_flags_of_the_flags_file(tmp_path):
    files = {"ch01/01-a.fail.cpp": "// expect-fail: x\n// passes-without: -Wnot-a-real-flag\nint main()\n{\n    return missing;\n}\n"}
    examples = make_tree(tmp_path, files)
    run = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_examples.py"), "--root", str(examples), "--flags-file", str(FIXTURES / "flags.txt"), "--skip-sanitizers", "--skip-format"],
        capture_output=True,
        text=True,
    )
    if COMPILERS:
        assert run.returncode == 1, run.stdout + run.stderr
        assert "'passes-without' names flags that are not in flags.txt" in run.stdout


@needs_compiler
def test_passes_without_must_really_make_the_program_build(tmp_path):
    files = {"ch01/01-a.fail.cpp": "// expect-fail: x\n// passes-without: -Werror\nint main()\n{\n    return missing;\n}\n"}
    examples = make_tree(tmp_path, files)
    run = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_examples.py"), "--root", str(examples), "--flags-file", str(FIXTURES / "flags.txt"), "--skip-sanitizers", "--skip-format"],
        capture_output=True,
        text=True,
    )
    assert run.returncode == 1, run.stdout + run.stderr
    assert "without -Werror it should build, but" in run.stdout


@needs_clang
def test_require_all_fails_when_a_compiler_is_missing():
    run = run_checker("good", "--require-all", env={"GXX": "no-such-compiler-xyz"}, sanitizers=True)
    assert run.returncode == 1, run.output
    assert "--require-all: gcc:" in run.output


def test_require_all_cannot_be_combined_with_skipping_a_check():
    for skip in ("--skip-sanitizers", "--skip-format"):
        run = run_checker("good", "--require-all", skip)
        assert run.returncode == 2, run.output
        assert "would silently drop a check" in run.output


def test_a_missing_flags_file_is_a_clear_message_not_a_traceback():
    run = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_examples.py"), "--root", str(FIXTURES / "good"), "--flags-file", str(FIXTURES / "no-such-flags.txt")],
        capture_output=True,
        text=True,
    )
    assert run.returncode == 1
    assert "does not exist" in run.stderr and "Traceback" not in run.stderr


def test_a_tree_without_programs_shows_why(tmp_path):
    examples = make_tree(tmp_path, {"ch01/05-sub/inner/main.cpp": MINIMAL, "ch01/stray.h": ""})
    run = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_examples.py"), "--root", str(examples), "--flags-file", str(FIXTURES / "flags.txt")],
        capture_output=True,
        text=True,
    )
    assert run.returncode == 1
    assert "No examples found." in run.stderr and "stray.h" in run.stderr


def test_a_targeted_run_of_a_broken_project_shows_the_cause(tmp_path):
    examples = make_tree(tmp_path, {"ch01/03-nomain/helper.cpp": MINIMAL, "ch01/01-ok.cpp": MINIMAL})
    run = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_examples.py"), "--root", str(examples), "--flags-file", str(FIXTURES / "flags.txt"), str(examples / "ch01" / "03-nomain")],
        capture_output=True,
        text=True,
    )
    assert run.returncode == 1
    assert "needs a main.cpp" in run.stderr


def test_files_the_system_adds_beside_programs_are_ignored(tmp_path):
    programs, problems = discover(tmp_path, {"ch01/01-a.cpp": MINIMAL, "ch01/._01-a.cpp": "binary junk"})
    assert problems == [] and len(programs) == 1
