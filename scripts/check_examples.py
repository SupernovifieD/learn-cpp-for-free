#!/usr/bin/env python3
"""Check every C++ example in examples/: it must build, run, print what the book says, and be formatted.

    python scripts/check_examples.py                 # all examples
    python scripts/check_examples.py --require-all   # CI: a missing compiler is a failure
    python scripts/check_examples.py examples/ch00/07-hello-world.cpp   # just these files

How each kind of file is judged, with the strict flags from examples/flags-gcc-clang.txt:

  X.cpp       must compile and link with ZERO diagnostics on every compiler, run for at most
              5 seconds (stdin comes from X.in when it exists) and exit with code 0.
              When X.out exists, standard output must match it byte for byte.
  X.fail.cpp  must FAIL to build on every compiler. Its first line must be
                  // expect-fail: <one-line reason>
              An optional second line
                  // passes-without: <flag> [<flag> ...]
              also makes the checker prove the file builds once those flags are removed, which
              shows the failure really comes from the flags the book teaches.

Every .cpp file must also have lines of at most 80 columns and be clang-format clean. Nothing is
written to the repository: builds happen in a temporary directory.

Compilers: "g++" must really be GCC and "clang++" must really be Clang. Apple's g++ is a copy of
Clang, so it is not counted as GCC; set GXX to a real GCC (for example GXX=g++-15) to test it.
Without --require-all a missing compiler is only a warning. The script needs nothing but Python 3
and the compilers (clang-format is found through the clang-format package or PATH).
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
EXAMPLES = REPO / "examples"
FLAGS_FILE = EXAMPLES / "flags-gcc-clang.txt"
MAX_COLUMNS = 80
RUN_TIMEOUT_SECONDS = 5
COMPILE_TIMEOUT_SECONDS = 120


@dataclass
class Compiler:
    """A C++ compiler found on this machine (kind is 'gcc' or 'clang')."""

    kind: str
    command: str
    version: str


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


def read_flags() -> list[str]:
    """The strict flags: the one line of examples/flags-gcc-clang.txt."""
    lines = [line for line in FLAGS_FILE.read_text().splitlines() if line.strip()]
    if len(lines) != 1:
        sys.exit(f"{FLAGS_FILE.relative_to(REPO)} must contain exactly one line, but has {len(lines)}.")
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


def build(compiler: Compiler, flags: list[str], source: Path, exe: Path) -> subprocess.CompletedProcess:
    """Compile and link `source` to `exe`, merging all diagnostics into one text."""
    command = [compiler.command, *flags, str(source), "-o", str(exe)]
    return subprocess.run(command, capture_output=True, text=True, timeout=COMPILE_TIMEOUT_SECONDS)


def directive(source: Path, name: str) -> str | None:
    """The value of a '// name: value' comment line at the top of a file, if present."""
    for line in source.read_text().splitlines()[:3]:
        prefix = f"// {name}:"
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return None


def check_program(compiler: Compiler, flags: list[str], source: Path, scratch: Path, result: Result) -> None:
    """X.cpp: builds cleanly, runs, exits 0, and prints exactly what X.out says."""
    column = compiler.kind
    exe = scratch / f"{source.stem}-{compiler.kind}"
    built = build(compiler, flags, source, exe)
    diagnostics = (built.stdout + built.stderr).strip()
    if built.returncode != 0 or diagnostics:
        result.fail(column, f"{compiler.command} reported problems (a clean build has no output at all):\n{indent(diagnostics)}")
        return
    stdin_file = source.with_suffix(".in")
    try:
        run = subprocess.run(
            [str(exe)],
            input=stdin_file.read_bytes() if stdin_file.exists() else b"",
            capture_output=True,
            timeout=RUN_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        result.fail(column, f"the program ran for more than {RUN_TIMEOUT_SECONDS} seconds.")
        return
    if run.returncode != 0:
        result.fail(column, f"the program exited with code {run.returncode}, expected 0.")
        return
    expected_file = source.with_suffix(".out")
    if expected_file.exists() and run.stdout != expected_file.read_bytes():
        result.fail(
            column,
            f"output differs from {expected_file.name}.\n      expected: {expected_file.read_bytes()[:200]!r}\n      actual:   {run.stdout[:200]!r}",
        )
        return
    result.cells[column] = "PASS"


def check_failing_program(compiler: Compiler, flags: list[str], source: Path, scratch: Path, result: Result) -> None:
    """X.fail.cpp: must not build, and must build once the 'passes-without' flags are removed."""
    column = compiler.kind
    exe = scratch / f"{source.stem}-{compiler.kind}"
    built = build(compiler, flags, source, exe)
    if built.returncode == 0:
        result.fail(column, f"{compiler.command} built this file, but it is marked '// expect-fail' (it must not build).")
        return
    removable = directive(source, "passes-without")
    if removable:
        remove = set(shlex.split(removable))
        unknown = remove - set(flags)
        if unknown:
            result.fail(column, f"'passes-without' names flags that are not in {FLAGS_FILE.name}: {sorted(unknown)}")
            return
        relaxed = build(compiler, [flag for flag in flags if flag not in remove], source, scratch / f"{source.stem}-{compiler.kind}-relaxed")
        if relaxed.returncode != 0:
            result.fail(
                column,
                f"without {' '.join(sorted(remove))} it should build, but {compiler.command} still fails:\n{indent(relaxed.stdout + relaxed.stderr)}",
            )
            return
    result.cells[column] = "PASS"


def check_style(source: Path, clang_format: str | None, result: Result) -> None:
    """At most 80 columns per line, and clang-format has nothing to change."""
    too_long = [
        f"line {number} has {len(line)} columns"
        for number, line in enumerate(source.read_text().splitlines(), start=1)
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
        [clang_format, "--dry-run", "--Werror", f"--style=file:{REPO / '.clang-format'}", str(source)],
        capture_output=True,
        text=True,
    )
    if check.returncode != 0:
        result.fail("format", f"clang-format would change this file (run `make format`):\n{indent(check.stderr)}")
    else:
        result.cells["format"] = "PASS"


def check_directives(source: Path, result: Result) -> None:
    """A .fail.cpp must say why it fails; a normal example must not carry those comments."""
    if source.name.endswith(".fail.cpp"):
        if directive(source, "expect-fail") is None:
            result.fail("rules", "a .fail.cpp file must start with the line '// expect-fail: <one-line reason>'.")
        if source.with_suffix("").with_suffix(".out").exists():
            result.fail("rules", "a .fail.cpp file cannot have an .out file; it never runs.")
    elif directive(source, "expect-fail") is not None or directive(source, "passes-without") is not None:
        result.fail("rules", "only files named *.fail.cpp may use '// expect-fail' or '// passes-without'.")


def find_stray_files(sources: list[Path]) -> list[str]:
    """.out and .in files with no program next to them."""
    stray = []
    for extra in sorted(EXAMPLES.rglob("*")):
        if extra.suffix in {".out", ".in"} and extra.with_suffix(".cpp") not in sources:
            stray.append(f"{extra.relative_to(REPO)} has no matching {extra.stem}.cpp")
        elif extra.is_file() and extra.suffix not in {".cpp", ".out", ".in", ".txt"}:
            stray.append(f"{extra.relative_to(REPO)} has an unexpected file type (examples/ holds .cpp, .out, .in and flags .txt files)")
    return stray


def check_one(source: Path, compilers: list[Compiler], flags: list[str], clang_format: str | None) -> Result:
    result = Result(str(source.relative_to(REPO)))
    expects_failure = source.name.endswith(".fail.cpp")
    check_directives(source, result)
    with tempfile.TemporaryDirectory(prefix="cppbook-example-") as tmp:
        for compiler in compilers:
            if expects_failure:
                check_failing_program(compiler, flags, source, Path(tmp), result)
            else:
                check_program(compiler, flags, source, Path(tmp), result)
    check_style(source, clang_format, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile, run and format-check the C++ examples.")
    parser.add_argument("files", nargs="*", type=Path, help="check only these files (default: every .cpp under examples/)")
    parser.add_argument("--require-all", action="store_true", help="fail when GCC, Clang or clang-format is missing (used in CI)")
    parser.add_argument("--skip-format", action="store_true", help="do not run clang-format (only for machines that cannot install it)")
    args = parser.parse_args()

    sources = sorted(p.resolve() for p in (args.files or EXAMPLES.rglob("*.cpp")))
    if not sources:
        sys.exit("No examples found.")
    for source in sources:
        if not source.is_file() or EXAMPLES not in source.parents or source.suffix != ".cpp":
            sys.exit(f"{source} is not a .cpp file inside examples/.")

    notes: list[str] = []
    found = find_compilers(notes)
    missing = [kind for kind, compiler in found.items() if compiler is None]
    compilers = [c for c in found.values() if c is not None]
    clang_format = None if args.skip_format else find_clang_format()
    if clang_format is None and not args.skip_format:
        notes.append("clang-format was not found (install requirements-dev.txt).")

    problems: list[str] = []
    if args.require_all:
        problems += [f"--require-all: {note}" for note in notes]
    flags = read_flags()
    print("Flags     :", " ".join(flags))
    for compiler in compilers:
        print(f"{compiler.kind.upper():<10}: {compiler.version} ({compiler.command})")
    for note in notes:
        print(("ERROR   " if args.require_all else "WARNING ") + note)
    print()

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda s: check_one(s, compilers, flags, clang_format), sources))

    columns = ["gcc", "clang", "80col", "format"]
    width = max(len(r.name) for r in results)
    print(f"{'example':<{width}}  " + "  ".join(f"{c:<6}" for c in columns))
    for r in results:
        cells = []
        for column in columns:
            default = "SKIP" if column in missing or (column == "format" and clang_format is None) else "-"
            cells.append(f"{r.cells.get(column, default):<6}")
        print(f"{r.name:<{width}}  " + "  ".join(cells))

    failures = [r for r in results if r.problems]
    for r in failures:
        print(f"\nFAIL {r.name}")
        for problem in r.problems:
            print("   " + problem)
    if not args.files:  # stray files are only meaningful when everything was checked
        problems += find_stray_files(sources)
    for problem in problems:
        print(f"\nFAIL {problem}")

    passed = len(results) - len(failures)
    print(f"\n{passed} of {len(results)} examples passed" + (", with problems elsewhere (see above)." if problems else "."))
    return 1 if failures or problems else 0


if __name__ == "__main__":
    sys.exit(main())
