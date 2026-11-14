#!/usr/bin/env python3
"""Check every C++ example in examples/: it must build, run, print what the book says, and be formatted.

    python scripts/check_examples.py                 # all examples
    python scripts/check_examples.py --require-all   # CI: a missing compiler or sanitizer is a failure
    python scripts/check_examples.py examples/ch00/07-hello-world.cpp   # just these programs
    python scripts/check_examples.py --root tests/scripts/fixtures/good --flags-file tests/scripts/fixtures/flags.txt

A program is either one file, examples/chNN/X.cpp, or a project: a folder examples/chNN/X/ that holds
.cpp files and the .h headers they include. Every .cpp file of a project is compiled and linked in
ONE command (the folder is flat, and one of the files is main.cpp). The files that belong to a program
sit NEXT TO it, whether it is a file or a folder: X.out, X.in and X.session.

How each program is judged, with the strict flags from examples/flags-gcc-clang.txt:

  X.cpp or X/        must compile and link with ZERO diagnostics on every compiler, run for at most
                     5 seconds (stdin comes from X.in when it exists) and exit with code 0, and
                     print what the book promises:
                       X.out      standard output must match it byte for byte;
                       X.session  what a reader SEES in a console when typing the lines of X.in:
                                  removing each X.in line, in order, from where it appears in
                                  X.session must leave exactly the program's standard output.
                     A program has X.out or X.session, never both, and X.in goes with X.session.
                     Then the same program is built again with the strict flags plus AddressSanitizer
                     and UBSan and run again: any sanitizer report is a failure ("san" column).
  X.fail.cpp or      must FAIL to build on every compiler. The first lines of the file (of main.cpp
  X.fail/            for a project) must contain
                         // expect-fail: <one-line reason>
                     and may contain
                         // passes-without: <flag> [<flag> ...]
                     which also makes the checker prove the program builds once those flags are
                     removed, which shows the failure really comes from the flags the book teaches.
                     A failing program never runs, so it has no X.out, X.in or X.session.

Every .cpp and .h file must also have lines of at most 80 columns and be clang-format clean. Nothing
is written to the repository: builds happen in a temporary directory.

Compilers: "g++" must really be GCC and "clang++" must really be Clang. Apple's g++ is a copy of
Clang, so it is not counted as GCC; set GXX to a real GCC (for example GXX=g++-15) to test it.
Without --require-all a missing compiler (or a compiler without sanitizer runtime) is only a warning.
The script needs nothing but Python 3 and the compilers (clang-format is found through the
clang-format package or PATH).
"""

from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = REPO / "examples"
FLAGS_NAME = "flags-gcc-clang.txt"
MAX_COLUMNS = 80
RUN_TIMEOUT_SECONDS = 5
SANITIZER_RUN_TIMEOUT_SECONDS = 10
COMPILE_TIMEOUT_SECONDS = 120
SANITIZER_FLAGS = ["-fsanitize=address,undefined", "-fno-sanitize-recover=all", "-g"]
COMPANION_SUFFIXES = (".out", ".in", ".session")
IGNORED_NAMES = {".DS_Store"}

# Two tiny programs that tell "this machine has no sanitizer runtime" and "this machine's sanitizers
# crash at start-up" apart from "an example has a real finding". The first allocates and frees; the
# second overflows a signed integer, which UBSan must report (and, with
# -fno-sanitize-recover=all, must answer with a non-zero exit code).
PROBE_CLEAN = """#include <iostream>
int main(int argc, char**)
{
    int* values = new int[4]{argc, 0, 0, 0};
    std::cout << values[0] << "\\n";
    delete[] values;
    return 0;
}
"""
PROBE_OVERFLOW = """int main(int argc, char**)
{
    int value = 2147483647;
    value += argc;
    return value == 0;
}
"""


@dataclass
class Compiler:
    """A C++ compiler found on this machine (kind is 'gcc' or 'clang')."""

    kind: str
    command: str
    version: str


@dataclass(frozen=True)
class Program:
    """One example program: a single file (X.cpp, X.fail.cpp) or a project folder (X/, X.fail/)."""

    base: Path
    is_project: bool
    sources: tuple[Path, ...]
    headers: tuple[Path, ...]

    @property
    def stem(self) -> str:
        """The name that its companions share: X for X.cpp and X/, X.fail for X.fail.cpp and X.fail/."""
        return self.base.name if self.is_project else self.base.name[: -len(".cpp")]

    @property
    def expects_failure(self) -> bool:
        return self.stem.endswith(".fail")

    @property
    def main_file(self) -> Path:
        return self.base / "main.cpp" if self.is_project else self.base

    @property
    def files(self) -> tuple[Path, ...]:
        return (*self.sources, *self.headers)

    def companion(self, suffix: str) -> Path:
        """X.out, X.in or X.session next to the program (not inside a project folder)."""
        return self.base.with_name(self.stem + suffix)


def identify(command: str) -> tuple[str, str] | None:
    """Return (kind, first version line) for a compiler command, or None when it is not installed."""
    path = shutil.which(command)
    if path is None:
        return None
    try:
        out = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.TimeoutExpired):
        return None
    first = out.splitlines()[0] if out else ""
    if "clang" in out.lower():
        return "clang", first
    if "g++" in first or "gcc" in first.lower() or "Free Software Foundation" in out:
        return "gcc", first
    return None


def find_compilers(notes: list[str]) -> dict[str, Compiler | None]:
    """Locate GCC and Clang. A name that points at the wrong compiler counts as missing."""
    found: dict[str, Compiler | None] = {}
    for kind, default in (("gcc", "g++"), ("clang", "clang++")):
        command = os.environ.get("GXX" if kind == "gcc" else "CLANGXX", default)
        info = identify(command)
        if info is None:
            notes.append(f"{kind}: '{command}' was not found on this machine.")
            found[kind] = None
        elif info[0] != kind:
            notes.append(
                f"{kind}: '{command}' is really {info[0]} ({info[1]}), so it does not count as {kind.upper()}. "
                f"Install GCC and point the {'GXX' if kind == 'gcc' else 'CLANGXX'} variable at it."
            )
            found[kind] = None
        else:
            found[kind] = Compiler(kind, command, info[1])
    return found


def find_clang_format() -> str | None:
    """The pinned clang-format from requirements-dev.txt, or one on PATH."""
    try:
        import clang_format  # type: ignore[import-not-found]

        return clang_format.get_executable("clang-format")
    except ImportError:
        return shutil.which("clang-format")


def read_flags(flags_file: Path) -> list[str]:
    """The strict flags: the one line of the flags file."""
    lines = [line for line in flags_file.read_text().splitlines() if line.strip()]
    if len(lines) != 1:
        sys.exit(f"{flags_file} must contain exactly one line, but has {len(lines)}.")
    return shlex.split(lines[0])


@dataclass
class Result:
    """What happened to one example."""

    name: str
    cells: dict[str, str] = field(default_factory=dict)  # column -> PASS / FAIL / SKIP / -
    problems: list[str] = field(default_factory=list)

    def fail(self, column: str, message: str) -> None:
        self.cells[column] = "FAIL"
        self.problems.append(f"[{column}] {message}")


def indent(text: str) -> str:
    return "\n".join("      " + line for line in text.strip().splitlines()[:25])


def display(path: Path, root: Path) -> str:
    """A path as shown in messages: relative to the folder that holds the examples folder."""
    try:
        return path.relative_to(root.parent).as_posix()
    except ValueError:
        return path.as_posix()


# --------------------------------------------------------------------- discovery --


def discover(root: Path) -> tuple[list[Program], list[str]]:
    """Find every program under root (root/chNN/...) and report files that do not belong anywhere."""
    programs: list[Program] = []
    problems: list[str] = []
    companions: list[Path] = []

    def shown(path: Path) -> str:
        return display(path, root)

    for top in sorted(root.iterdir()):
        if top.name in IGNORED_NAMES:
            continue
        if top.is_file():
            if top.suffix != ".txt":
                problems.append(
                    f"{shown(top)} is not allowed directly in {root.name}/ (only the flags .txt file is); "
                    f"put programs in a chapter folder such as {root.name}/ch01/."
                )
            continue
        for entry in sorted(top.iterdir()):
            if entry.name in IGNORED_NAMES:
                continue
            if entry.is_dir():
                project = discover_project(entry, shown, problems)
                if project:
                    programs.append(project)
            elif entry.suffix == ".cpp":
                programs.append(Program(entry, False, (entry,), ()))
            elif entry.suffix in COMPANION_SUFFIXES:
                companions.append(entry)
            elif entry.suffix == ".h":
                problems.append(
                    f"{shown(entry)}: .h files may only live inside a project folder; "
                    f"move it next to the .cpp files that include it, in a folder such as {entry.stem}/."
                )
            else:
                problems.append(
                    f"{shown(entry)} has an unexpected file type (a chapter folder holds .cpp files, project folders "
                    f"and the .out, .in and .session files of programs)."
                )

    seen: dict[tuple[Path, str], Program] = {}
    for program in programs:
        key = (program.base.parent, program.stem)
        if key in seen:
            problems.append(f"{shown(program.base)} and {shown(seen[key].base)} have the same name; a program is either a file or a folder.")
        seen[key] = program
    for companion in companions:
        stem = companion.name[: -len(companion.suffix)]
        if (companion.parent, stem) not in seen:
            problems.append(
                f"{shown(companion)} has no matching program: expected {stem}.cpp or a folder {stem}/ in the same chapter folder."
            )
    return programs, problems


def discover_project(folder: Path, shown, problems: list[str]) -> Program | None:
    """A project folder is flat: .cpp and .h files, one of them main.cpp."""
    sources: list[Path] = []
    headers: list[Path] = []
    for item in sorted(folder.iterdir()):
        if item.name in IGNORED_NAMES:
            continue
        if item.is_dir():
            problems.append(f"{shown(item)}/ is a folder inside a project; a project folder is flat, so move its files up.")
        elif item.suffix == ".cpp":
            sources.append(item)
        elif item.suffix == ".h":
            headers.append(item)
        else:
            problems.append(
                f"{shown(item)} has an unexpected file type inside a project folder (only .cpp and .h files; "
                f"put {folder.name}.out, {folder.name}.in and {folder.name}.session NEXT TO the folder)."
            )
    if folder / "main.cpp" not in sources:
        problems.append(f"{shown(folder)}/ needs a main.cpp (the project's entry point), but has none.")
        return None
    return Program(folder, True, tuple(sources), tuple(headers))


def select_programs(targets: list[Path], programs: list[Program], root: Path) -> list[Program]:
    """Map command-line arguments (a file, a project folder or a file inside one) to programs."""
    if not targets:
        return programs
    chosen: list[Program] = []
    for target in targets:
        resolved = target.resolve()
        match = next((p for p in programs if resolved == p.base or resolved in p.files), None)
        if match is None:
            sys.exit(f"{target} is not a program, a project folder or a file of a project inside {root}.")
        if match not in chosen:
            chosen.append(match)
    return chosen


# ------------------------------------------------------------------------ sessions --


def prove_session(session: bytes, typed: bytes, stdout: bytes, names: tuple[str, str] = ("X.in", "X.session")) -> str | None:
    """Prove that `session` is the program's `stdout` with the `typed` lines mixed in. None means proven.

    Removing each typed line (with its newline), in order, from where it appears in the session must
    leave exactly stdout, and every typed line must be found. A line the reader typed may look like text
    the program prints, so instead of deleting greedily this walks every consistent way to read the
    session: from (offset i in the session, k typed lines found so far), the next bytes are either
    typed line k or the next byte of stdout (which is at offset i - length of the first k typed lines).
    """
    lines = typed.splitlines(keepends=True)
    count = len(lines)
    consumed = [0]
    for line in lines:
        consumed.append(consumed[-1] + len(line))
    reach: list[set[int]] = [set() for _ in range(len(session) + 1)]
    reach[0].add(0)
    farthest = 0
    for i in range(len(session) + 1):
        if not reach[i]:
            continue
        farthest = i
        for k in reach[i]:
            if k < count and session.startswith(lines[k], i):
                reach[i + len(lines[k])].add(k + 1)
            j = i - consumed[k]
            if i < len(session) and j < len(stdout) and session[i] == stdout[j]:
                reach[i + 1].add(k)
    if count in reach[len(session)] and len(session) - consumed[count] == len(stdout):
        return None

    k = max(reach[farthest])
    j = farthest - consumed[k]
    typed_name, session_name = names
    if farthest == len(session):
        if k < count:
            return (
                f"typed line {k + 1} of {typed_name} ({lines[k].decode(errors='replace').rstrip()!r}) does not appear in {session_name}; "
                f"every line the reader types must be shown where it is typed."
            )
        return f"{session_name} ends too early: the program also prints {stdout[j:][:60].decode(errors='replace')!r}."
    number = session.count(b"\n", 0, farthest) + 1
    start = session.rfind(b"\n", 0, farthest) + 1
    end = session.find(b"\n", farthest)
    shown_line = session[start : end if end != -1 else len(session)].decode(errors="replace")
    # Show the program's text from where the session line began, so the difference is easy to see.
    context = stdout[max(0, j - (farthest - start)) : j + 40].decode(errors="replace")
    options = [f"the program prints {context!r}"] if j < len(stdout) else []
    if k < count:
        options.append(f"the reader types {lines[k].decode(errors='replace').rstrip()!r} (typed line {k + 1} of {typed_name})")
    return f"line {number} of {session_name} reads {shown_line!r}, but at this point " + (" or ".join(options) or "nothing more is printed or typed") + "."


def judge_stdout(program: Program, stdout: bytes) -> str | None:
    """None when standard output is what the book promises for this program, otherwise a message."""
    session = program.companion(".session")
    if session.exists():
        typed_file = program.companion(".in")
        typed = typed_file.read_bytes() if typed_file.exists() else b""
        return prove_session(session.read_bytes(), typed, stdout, (typed_file.name, session.name))
    expected_file = program.companion(".out")
    if expected_file.exists() and stdout != expected_file.read_bytes():
        return f"output differs from {expected_file.name}.\n      expected: {expected_file.read_bytes()[:200]!r}\n      actual:   {stdout[:200]!r}"
    return None


# ------------------------------------------------------------------------ building --


def build(compiler: Compiler, flags: list[str], sources: tuple[Path, ...], exe: Path, cwd: Path) -> subprocess.CompletedProcess:
    """Compile and link all `sources` into `exe`, merging all diagnostics into one text."""
    command = [compiler.command, *flags, *(str(source) for source in sorted(sources)), "-o", str(exe)]
    return subprocess.run(command, capture_output=True, text=True, timeout=COMPILE_TIMEOUT_SECONDS, cwd=cwd)


def directive(source: Path, name: str) -> str | None:
    """The value of a '// name: value' comment line at the top of a file, if present."""
    for line in source.read_text().splitlines()[:3]:
        prefix = f"// {name}:"
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return None


def run_and_judge(exe: Path, program: Program, timeout: int, cwd: Path) -> str | None:
    """Run a built program with X.in on stdin; None when it exits 0 and prints what the book promises."""
    stdin_file = program.companion(".in")
    try:
        run = subprocess.run(
            [str(exe)],
            input=stdin_file.read_bytes() if stdin_file.exists() else b"",
            capture_output=True,
            timeout=timeout,
            cwd=cwd,
        )
    except subprocess.TimeoutExpired:
        return f"the program ran for more than {timeout} seconds."
    if run.returncode != 0:
        return f"the program exited with code {run.returncode}, expected 0.\n{indent(run.stderr.decode(errors='replace'))}".rstrip()
    return judge_stdout(program, run.stdout)


def check_program(compiler: Compiler, flags: list[str], program: Program, scratch: Path, result: Result) -> bool:
    """X.cpp or X/: builds cleanly, runs, exits 0, and prints what X.out or X.session promises."""
    column = compiler.kind
    exe = scratch / f"{program.stem}-{compiler.kind}"
    built = build(compiler, flags, program.sources, exe, scratch)
    diagnostics = (built.stdout + built.stderr).strip()
    if built.returncode != 0 or diagnostics:
        hint = ""
        if built.returncode != 0:
            ending = "/" if program.is_project else ".cpp"
            hint = (
                f"\n      If this program is meant to fail, rename it {program.stem}.fail{ending} "
                f"and start {program.main_file.name} with '// expect-fail: <reason>'."
            )
        result.fail(column, f"{compiler.command} reported problems (a clean build has no output at all):\n{indent(diagnostics)}{hint}")
        return False
    problem = run_and_judge(exe, program, RUN_TIMEOUT_SECONDS, scratch)
    if problem:
        result.fail(column, problem)
        return False
    result.cells[column] = "PASS"
    return True


def check_sanitized(compiler: Compiler, flags: list[str], program: Program, scratch: Path, result: Result) -> bool:
    """The same program built with AddressSanitizer and UBSan: it must still build, run and print the same."""
    exe = scratch / f"{program.stem}-{compiler.kind}-san"
    built = build(compiler, [*flags, *SANITIZER_FLAGS], program.sources, exe, scratch)
    if built.returncode != 0:
        result.fail("san", f"{compiler.command} could not build this program with the sanitizers:\n{indent(built.stdout + built.stderr)}")
        return False
    problem = run_and_judge(exe, program, SANITIZER_RUN_TIMEOUT_SECONDS, scratch)
    if problem:
        result.fail("san", f"{compiler.command} with AddressSanitizer and UBSan: {problem}")
        return False
    return True


def check_failing_program(compiler: Compiler, flags: list[str], flags_name: str, program: Program, scratch: Path, result: Result) -> None:
    """X.fail.cpp or X.fail/: must not build, and must build once the 'passes-without' flags are removed."""
    column = compiler.kind
    exe = scratch / f"{program.stem}-{compiler.kind}"
    built = build(compiler, flags, program.sources, exe, scratch)
    if built.returncode == 0:
        result.fail(column, f"{compiler.command} built this program, but it is marked as failing ('.fail' in its name): it must not build.")
        return
    removable = directive(program.main_file, "passes-without")
    if removable:
        remove = set(shlex.split(removable))
        unknown = remove - set(flags)
        if unknown:
            result.fail(column, f"'passes-without' names flags that are not in {flags_name}: {sorted(unknown)}")
            return
        relaxed = build(compiler, [flag for flag in flags if flag not in remove], program.sources, scratch / f"{program.stem}-{compiler.kind}-relaxed", scratch)
        if relaxed.returncode != 0:
            result.fail(
                column,
                f"without {' '.join(sorted(remove))} it should build, but {compiler.command} still fails:\n{indent(relaxed.stdout + relaxed.stderr)}",
            )
            return
    result.cells[column] = "PASS"


def probe_sanitizers(compiler: Compiler, scratch: Path) -> str | None:
    """None when this compiler can build and run programs with the sanitizers, else the reason it cannot."""
    flags = ["-std=c++20", *SANITIZER_FLAGS]
    clean_source = scratch / f"probe-clean-{compiler.kind}.cpp"
    clean_source.write_text(PROBE_CLEAN)
    clean = build(compiler, flags, (clean_source,), scratch / f"probe-clean-{compiler.kind}", scratch)
    if clean.returncode != 0:
        return (
            f"{compiler.command} cannot build with -fsanitize=address,undefined, so its sanitizer runtime is probably not installed "
            f"(on Ubuntu: libasan and libubsan for GCC, libclang-rt-<version>-dev for Clang):\n{indent(clean.stdout + clean.stderr)}"
        )
    try:
        ran = subprocess.run([str(scratch / f"probe-clean-{compiler.kind}")], capture_output=True, timeout=SANITIZER_RUN_TIMEOUT_SECONDS, cwd=scratch)
    except subprocess.TimeoutExpired:
        return "a trivial program built with the sanitizers did not finish."
    if ran.returncode != 0:
        return (
            f"a trivial program built with {compiler.command} and the sanitizers crashes at start-up, so the sanitizers cannot run here "
            f"(on Linux this is usually the high ASLR entropy problem; `sudo sysctl -w vm.mmap_rnd_bits=28` is the documented fix):\n"
            f"{indent(ran.stderr.decode(errors='replace'))}"
        )
    overflow_source = scratch / f"probe-overflow-{compiler.kind}.cpp"
    overflow_source.write_text(PROBE_OVERFLOW)
    overflow = build(compiler, flags, (overflow_source,), scratch / f"probe-overflow-{compiler.kind}", scratch)
    if overflow.returncode != 0:
        return f"{compiler.command} could not build the UBSan probe:\n{indent(overflow.stdout + overflow.stderr)}"
    found = subprocess.run([str(scratch / f"probe-overflow-{compiler.kind}")], capture_output=True, timeout=SANITIZER_RUN_TIMEOUT_SECONDS, cwd=scratch)
    if found.returncode == 0:
        return f"{compiler.command} did not report a signed integer overflow with -fsanitize=undefined, so UBSan does not work here."
    return None


# --------------------------------------------------------------------------- rules --


def check_style(program: Program, clang_format: str | None, result: Result) -> None:
    """At most 80 columns per line in every file of the program, and clang-format has nothing to change."""

    def label(path: Path) -> str:
        return f"{path.relative_to(program.base).as_posix()}: " if program.is_project else ""

    too_long = [
        f"{label(path)}line {number} has {len(line)} columns"
        for path in program.files
        for number, line in enumerate(path.read_text().splitlines(), start=1)
        if len(line) > MAX_COLUMNS
    ]
    if too_long:
        result.fail("80col", f"limit is {MAX_COLUMNS}: " + "; ".join(too_long[:5]))
    else:
        result.cells["80col"] = "PASS"
    if clang_format is None:
        result.cells["format"] = "SKIP"
        return
    check = subprocess.run(
        [clang_format, "--dry-run", "--Werror", f"--style=file:{REPO / '.clang-format'}", *(str(path) for path in program.files)],
        capture_output=True,
        text=True,
    )
    if check.returncode != 0:
        result.fail("format", f"clang-format would change this program (run `make format`):\n{indent(check.stderr)}")
    else:
        result.cells["format"] = "PASS"


def check_rules(program: Program, result: Result) -> None:
    """The naming and companion-file rules that do not need a compiler."""
    main = program.main_file
    if program.expects_failure:
        if directive(main, "expect-fail") is None:
            where = "main.cpp of the project" if program.is_project else "the file"
            result.fail("rules", f"a failing program must start {where} with the line '// expect-fail: <one-line reason>'.")
    else:
        for path in program.files:
            if directive(path, "expect-fail") is not None or directive(path, "passes-without") is not None:
                result.fail(
                    "rules",
                    f"{path.name}: only failing programs (named X.fail.cpp or X.fail/) may use '// expect-fail' or '// passes-without'; "
                    f"if this program must fail, rename it.",
                )
                break

    out, typed, session = (program.companion(suffix) for suffix in COMPANION_SUFFIXES)
    if program.expects_failure:
        for extra in (out, typed, session):
            if extra.exists():
                result.fail("rules", f"{extra.name}: a failing program never runs, so it cannot have an {extra.suffix} file; delete it.")
        return
    if out.exists() and session.exists():
        result.fail("rules", f"{out.name} and {session.name} cannot both exist: a program that reads input shows its session, any other program its output; delete one.")
    if session.exists() and not typed.exists():
        result.fail("rules", f"{session.name} needs {typed.name}, the lines the reader types, one per Enter press.")
    if typed.exists() and not session.exists():
        result.fail("rules", f"{typed.name} needs {session.name}: a program that reads input shows what the reader sees in the console, so replace {out.name} by {session.name}.")
    for file in (typed, session):
        if file.exists():
            data = file.read_bytes()
            if b"\r" in data or (data and not data.endswith(b"\n")):
                result.fail("rules", f"{file.name} must use \\n line endings (no \\r) and end with a newline.")


def check_one(
    program: Program,
    compilers: list[Compiler],
    flags: list[str],
    flags_name: str,
    clang_format: str | None,
    sanitizers: set[str],
    root: Path,
) -> Result:
    result = Result(display(program.base, root) + ("/" if program.is_project else ""))
    check_rules(program, result)
    ran_sanitized = False
    with tempfile.TemporaryDirectory(prefix="cppbook-example-") as tmp:
        scratch = Path(tmp)
        for compiler in compilers:
            if program.expects_failure:
                check_failing_program(compiler, flags, flags_name, program, scratch, result)
            elif check_program(compiler, flags, program, scratch, result) and compiler.kind in sanitizers:
                ran_sanitized = True
                check_sanitized(compiler, flags, program, scratch, result)
    if program.expects_failure:
        result.cells["san"] = "-"
    elif ran_sanitized and "san" not in result.cells:
        result.cells["san"] = "PASS"
    check_style(program, clang_format, result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile, run, sanitize and format-check the C++ examples.")
    parser.add_argument("targets", nargs="*", type=Path, metavar="PROGRAM", help="check only these programs: a .cpp file, a project folder or a file inside one (default: every program under the root)")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="the folder that holds the chapter folders (default: examples/)")
    parser.add_argument("--flags-file", type=Path, default=None, help=f"the file with the strict flags (default: <root>/{FLAGS_NAME})")
    parser.add_argument("--require-all", action="store_true", help="fail when GCC, Clang, a sanitizer runtime or clang-format is missing (used in CI)")
    parser.add_argument("--skip-format", action="store_true", help="do not run clang-format (only for machines that cannot install it)")
    parser.add_argument("--skip-sanitizers", action="store_true", help="do not build and run the programs with AddressSanitizer and UBSan")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        sys.exit(f"{args.root} is not a folder.")
    flags_file = (args.flags_file or root / FLAGS_NAME).resolve()
    programs, structure_problems = discover(root)
    if not programs:
        sys.exit("No examples found.")
    selected = select_programs(args.targets, programs, root)

    notes: list[str] = []
    found = find_compilers(notes)
    missing = [kind for kind, compiler in found.items() if compiler is None]
    compilers = [c for c in found.values() if c is not None]
    clang_format = None if args.skip_format else find_clang_format()
    if clang_format is None and not args.skip_format:
        notes.append("clang-format was not found (install requirements-dev.txt).")

    sanitizers: set[str] = set()
    if not args.skip_sanitizers:
        with tempfile.TemporaryDirectory(prefix="cppbook-probe-") as tmp:
            for compiler in compilers:
                reason = probe_sanitizers(compiler, Path(tmp))
                if reason is None:
                    sanitizers.add(compiler.kind)
                else:
                    notes.append(f"{compiler.kind} sanitizers: {reason}")

    problems: list[str] = []
    if args.require_all:
        problems += [f"--require-all: {note}" for note in notes]
    flags = read_flags(flags_file)
    print("Flags     :", " ".join(flags))
    for compiler in compilers:
        print(f"{compiler.kind.upper():<10}: {compiler.version} ({compiler.command})")
    for note in notes:
        print(("ERROR   " if args.require_all else "WARNING ") + note)
    print()

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda p: check_one(p, compilers, flags, flags_file.name, clang_format, sanitizers, root), selected))

    columns = ["gcc", "clang", "san", "80col", "format"]
    width = max(len(r.name) for r in results)
    print(f"{'example':<{width}}  " + "  ".join(f"{c:<6}" for c in columns))
    for r in results:
        cells = []
        for column in columns:
            skipped = column in missing or (column == "format" and clang_format is None) or (column == "san" and not sanitizers)
            cells.append(f"{r.cells.get(column, 'SKIP' if skipped else '-'):<6}")
        print(f"{r.name:<{width}}  " + "  ".join(cells))

    failures = [r for r in results if r.problems]
    for r in failures:
        print(f"\nFAIL {r.name}")
        for problem in r.problems:
            print("   " + problem)
    if not args.targets:  # files that belong to no program are only meaningful when everything was checked
        problems += structure_problems
    for problem in problems:
        print(f"\nFAIL {problem}")

    passed = len(results) - len(failures)
    print(f"\n{passed} of {len(results)} examples passed" + (", with problems elsewhere (see above)." if problems else "."))
    return 1 if failures or problems else 0


if __name__ == "__main__":
    sys.exit(main())
