#!/usr/bin/env python3
"""mdBook preprocessor for the book syntax that mdBook does not have itself.

mdBook runs this script for every build (see [preprocessor.cppbook] in book.toml). It needs only
Python 3. Everything it writes is plain HTML around ordinary Markdown, so the pages still read
correctly without JavaScript.

1. Labeled code blocks. A fence with a title

       ```cpp title="hello-world.cpp"

   becomes a <figure class="listing"> with the label above the code, the same markup the Rust book
   uses for its listings. A title that is a file name is shown as "Filename: hello-world.cpp"; any
   other title (such as "Output") is shown as written.

2. Callouts that mdBook does not know. mdBook renders `> [!NOTE]`, `> [!TIP]` and `> [!WARNING]`
   itself. The kinds in CUSTOM_CALLOUTS get the same markup with their own title and icon.

3. Tabs.

       {{#tabs}}
       {{#tab Windows}}
       ...Markdown...
       {{#endtab}}
       {{#tab macOS}}
       ...Markdown...
       {{#endtab}}
       {{#endtabs}}

   becomes one labeled <section> per tab. theme/tabs.js turns the group into an accessible set of
   tabs; without JavaScript the sections are simply shown one after another.

4. Charts and data tables whose values come from checked example output.

       {{#chart bar ../examples/ch06/01-values.out x="Pass" y="Value" caption="Values by pass"}}
       {{#table ../examples/ch06/01-values.out header="Pass | Value"}}

   The chart becomes a Mermaid chart followed by the same data in a table. A table directive
   becomes an ordinary Markdown table. Both forms stop the build if the named checked companion
   or its data is invalid.

scripts/lint_content.py imports the patterns below, so the linter and the build agree on the syntax.
"""

from __future__ import annotations

import html
import json
import re
import shlex
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*(.*)$")
TITLED_INFO = re.compile(r'^(?P<language>[\w+-]+)\s+title="(?P<title>[^"]*)"\s*$')
FILE_NAME = re.compile(r"^[\w.-]+\.[A-Za-z0-9]+$")
CALLOUT = re.compile(r"^>\s*\[!(?P<kind>[A-Za-z-]+)\]\s*$")
TABS_OPEN = re.compile(r"^\{\{#tabs\}\}\s*$")
TABS_CLOSE = re.compile(r"^\{\{#endtabs\}\}\s*$")
TAB_OPEN = re.compile(r"^\{\{#tab\s+(?P<label>[^{}]+?)\s*\}\}\s*$")
TAB_CLOSE = re.compile(r"^\{\{#endtab\}\}\s*$")
CHART_DIRECTIVE = re.compile(r"^\{\{#chart\s+(?P<body>.*?)\}\}\s*$")
TABLE_DIRECTIVE = re.compile(r"^\{\{#table\s+(?P<body>.*?)\}\}\s*$")
VISUAL_DIRECTIVE = re.compile(r"\{\{#(?:chart|table)\b")

REPO = Path(__file__).resolve().parents[1]
CHECKED_DATA_SUFFIXES = {".out", ".err", ".example"}
MAX_CHART_ROWS = 12
MAX_TABLE_ROWS = 16

# Callouts that mdBook renders on its own.
NATIVE_CALLOUTS = {"NOTE", "TIP", "WARNING"}

# kind -> (title, path of a 16x16 icon). The icons are GitHub Octicons (MIT License), the set that
# mdBook uses for its own callouts: stop, check-circle, light-bulb and mortar-board.
CUSTOM_CALLOUTS = {
    "DANGER": (
        "Danger",
        "M4.47.22A.749.749 0 0 1 5 0h6c.199 0 .389.079.53.22l4.25 4.25c.141.14.22.331.22.53v6a.749.749 0 0 1-.22.53l-4.25 4.25A.749.749 0 0 1 11 16H5a.749.749 0 0 1-.53-.22L.22 11.53A.749.749 0 0 1 0 11V5c0-.199.079-.389.22-.53Zm.84 1.28L1.5 5.31v5.38l3.81 3.81h5.38l3.81-3.81V5.31L10.69 1.5ZM8 4a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 8 4Zm0 8a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z",
    ),
    "BEST-PRACTICE": (
        "Best practice",
        "M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm1.5 0a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm10.28-1.72-4.5 4.5a.75.75 0 0 1-1.06 0l-2-2a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018l1.47 1.47 3.97-3.97a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z",
    ),
    "KEY-INSIGHT": (
        "Key insight",
        "M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.766 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.516-.701 2.5-1.328 3.259-.095.115-.184.22-.268.319-.207.245-.383.453-.541.681-.208.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.985-1.32.985-2.304 0-2.06-1.637-3.75-4-3.75ZM5.75 12h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM6 15.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z",
    ),
    "ADVANCED": (
        "For advanced readers",
        "M7.693 1.066a.747.747 0 0 1 .614 0l7.25 3.25a.75.75 0 0 1 0 1.368L13 6.831v2.794c0 1.024-.81 1.749-1.66 2.173-.893.447-2.075.702-3.34.702-.278 0-.55-.012-.816-.036a.75.75 0 0 1 .133-1.494c.22.02.45.03.683.03 1.082 0 2.025-.221 2.67-.543.69-.345.83-.682.83-.832V7.503L8.307 8.934a.747.747 0 0 1-.614 0L4 7.28v1.663c.296.105.575.275.812.512.438.438.688 1.059.688 1.796v3a.75.75 0 0 1-.75.75h-3a.75.75 0 0 1-.75-.75v-3c0-.737.25-1.358.688-1.796.237-.237.516-.407.812-.512V6.606L.443 5.684a.75.75 0 0 1 0-1.368ZM2.583 5 8 7.428 13.416 5 8 2.572ZM2.5 11.25v2.25H4v-2.25c0-.388-.125-.611-.25-.735a.697.697 0 0 0-.5-.203.707.707 0 0 0-.5.203c-.125.124-.25.347-.25.735Z",
    ),
}


class SyntaxProblem(Exception):
    """A mistake in custom book syntax. The build stops and shows the page and line."""

    def __init__(self, line: int, message: str) -> None:
        super().__init__(message)
        self.line = line


@dataclass(frozen=True)
class ChartSpec:
    kind: str
    data_file: str
    x_title: str
    y_title: str
    caption: str
    skip: int


@dataclass(frozen=True)
class TableSpec:
    data_file: str
    headers: tuple[str, ...]
    skip: int


VisualSpec = ChartSpec | TableSpec


def _directive_label(name: str) -> str:
    return f"{{{{#{name}}}}}"


def _parts(line: str, number: int, directive: str, pattern: re.Pattern[str]) -> list[str]:
    match = pattern.fullmatch(line)
    if not match:
        raise SyntaxProblem(number, f"the {_directive_label(directive)} directive must occupy one complete line and end with }}}}.")
    try:
        return shlex.split(match["body"])
    except ValueError as problem:
        raise SyntaxProblem(number, f"cannot parse the {_directive_label(directive)} directive: {problem}.") from problem


def _attributes(tokens: list[str], number: int, directive: str, required: set[str]) -> tuple[dict[str, str], int]:
    values: dict[str, str] = {}
    skip: int | None = None
    for token in tokens:
        name, separator, value = token.partition("=")
        if not separator:
            raise SyntaxProblem(
                number,
                f"{token!r} in the {_directive_label(directive)} directive needs a name and value, "
                f'such as {sorted(required)[0]}="...".',
            )
        if name not in required | {"skip"}:
            allowed = ", ".join(sorted(required | {"skip"}))
            raise SyntaxProblem(number, f"unknown {name!r} option in the {_directive_label(directive)} directive; use {allowed}.")
        if name in values or (name == "skip" and skip is not None):
            raise SyntaxProblem(number, f"the {_directive_label(directive)} directive gives {name!r} more than once.")
        if not value:
            raise SyntaxProblem(number, f"the {name!r} option in the {_directive_label(directive)} directive cannot be empty.")
        if name == "skip":
            if not value.isdecimal():
                raise SyntaxProblem(number, "skip must be a non-negative whole number, such as skip=1.")
            skip = int(value)
        else:
            values[name] = value
    missing = required - values.keys()
    if missing:
        raise SyntaxProblem(number, f"the {_directive_label(directive)} directive is missing: {', '.join(sorted(missing))}.")
    return values, skip or 0


def parse_visual_directive(line: str, number: int) -> VisualSpec | None:
    """Parse one chart or table directive, or return None for an ordinary line."""
    if not VISUAL_DIRECTIVE.search(line):
        return None
    if line != line.lstrip():
        raise SyntaxProblem(number, "chart and table directives must start at the beginning of the line.")
    if line.startswith("{{#chart"):
        parts = _parts(line, number, "chart", CHART_DIRECTIVE)
        if len(parts) < 2:
            raise SyntaxProblem(number, 'write a chart as {{#chart bar|line <data-file> x="..." y="..." caption="..."}}.')
        kind, data_file, *option_tokens = parts
        if kind not in {"bar", "line"}:
            raise SyntaxProblem(number, f"unknown chart kind {kind!r}; use bar or line.")
        values, skip = _attributes(option_tokens, number, "chart", {"x", "y", "caption"})
        return ChartSpec(kind, data_file, values["x"], values["y"], values["caption"], skip)
    if line.startswith("{{#table"):
        parts = _parts(line, number, "table", TABLE_DIRECTIVE)
        if not parts:
            raise SyntaxProblem(number, 'write a table as {{#table <data-file> header="Column 1 | Column 2"}}.')
        data_file, *option_tokens = parts
        values, skip = _attributes(option_tokens, number, "table", {"header"})
        headers = tuple(part.strip() for part in values["header"].split("|"))
        if not 1 <= len(headers) <= 3:
            raise SyntaxProblem(number, "a generated table needs between 1 and 3 header columns, separated with |.")
        if any(not header for header in headers):
            raise SyntaxProblem(number, "every generated table column needs a non-empty header between the | separators.")
        return TableSpec(data_file, headers, skip)
    raise SyntaxProblem(number, "chart and table directives must occupy one complete line.")


def checked_data_file(spec: VisualSpec, source_path: Path, repo_root: Path, number: int) -> Path:
    """Resolve a directive's data file and prove that the example checker owns it."""
    target = (source_path.parent / spec.data_file).resolve()
    if not target.is_file():
        raise SyntaxProblem(number, f"the data file {spec.data_file!r} does not exist (the path is relative to this page).")
    if target.suffix not in CHECKED_DATA_SUFFIXES:
        allowed = ", ".join(sorted(CHECKED_DATA_SUFFIXES))
        raise SyntaxProblem(number, f"{spec.data_file!r} is not a checked output companion; use a file ending in {allowed}.")
    examples = (repo_root / "examples").resolve()
    try:
        target.relative_to(examples)
    except ValueError as problem:
        raise SyntaxProblem(number, f"{spec.data_file!r} is outside examples/ and therefore is not checked program output.") from problem
    source = target.with_suffix(".cpp")
    project = target.with_suffix("")
    valid_project = project.is_dir() and (project / "main.cpp").is_file()
    if not source.is_file() and not valid_project:
        raise SyntaxProblem(
            number,
            f"{spec.data_file!r} has no checked program; add {source.name} or a project folder named "
            f"{project.name}/ with main.cpp beside it.",
        )
    if target.suffix == ".example" and not target.with_suffix(".match").is_file():
        raise SyntaxProblem(number, f"{spec.data_file!r} needs {target.with_suffix('.match').name} beside it so varying output is checked.")
    return target


def program_files_for_data(data_file: Path) -> tuple[Path, ...]:
    """Return the source files that a page must show for this checked companion."""
    source = data_file.with_suffix(".cpp")
    if source.is_file():
        return (source,)
    project = data_file.with_suffix("")
    return tuple(sorted(path for path in project.iterdir() if path.suffix in {".cpp", ".h"}))


def _data_lines(data_file: Path, skip: int, number: int) -> list[str]:
    lines = data_file.read_text().splitlines()[skip:]
    if not lines:
        raise SyntaxProblem(number, f"{data_file.name} has no data rows after skip={skip}.")
    return lines


def _decimal(token: str, data_file: Path, row: int, number: int) -> Decimal:
    try:
        value = Decimal(token)
    except InvalidOperation as problem:
        raise SyntaxProblem(number, f"{data_file.name} data row {row} has non-number {token!r}.") from problem
    if not value.is_finite():
        raise SyntaxProblem(number, f"{data_file.name} data row {row} has non-finite number {token!r}; charts need finite values.")
    return value


def _markdown_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|")


def _markdown_table(headers: tuple[str, ...], rows: list[list[str]], numeric_last: bool = False) -> list[str]:
    heading = "| " + " | ".join(_markdown_cell(header) for header in headers) + " |"
    rules = ["---"] * len(headers)
    if numeric_last:
        rules[-1] = "---:"
    divider = "| " + " | ".join(rules) + " |"
    body = ["| " + " | ".join(_markdown_cell(value) for value in row) + " |" for row in rows]
    return [heading, divider, *body]


def _axis_number(value: Decimal) -> str:
    result = format(value, "f")
    if "." in result:
        result = result.rstrip("0").rstrip(".")
    return result or "0"


def _chart_range(kind: str, values: list[Decimal]) -> tuple[Decimal, Decimal]:
    if kind == "bar":
        return Decimal(0), max(max(values), Decimal(1))
    low, high = min(values), max(values)
    if low == high:
        padding = max(abs(low) * Decimal("0.1"), Decimal(1))
        return low - padding, high + padding
    return low, high


def render_visual_directive(spec: VisualSpec, source_path: Path, repo_root: Path, number: int) -> list[str]:
    """Turn one parsed directive into Mermaid or Markdown after validating its checked data."""
    data_file = checked_data_file(spec, source_path, repo_root, number)
    lines = _data_lines(data_file, spec.skip, number)
    if isinstance(spec, TableSpec):
        if len(lines) > MAX_TABLE_ROWS:
            raise SyntaxProblem(
                number,
                f"{data_file.name} has {len(lines)} data rows after skip={spec.skip}; "
                f"generated tables allow at most {MAX_TABLE_ROWS}.",
            )
        rows = [line.split() for line in lines]
        for row_number, row in enumerate(rows, start=spec.skip + 1):
            if len(row) != len(spec.headers):
                raise SyntaxProblem(
                    number,
                    f"{data_file.name} data row {row_number} has {len(row)} fields; "
                    f"its header has {len(spec.headers)} columns.",
                )
        return _markdown_table(spec.headers, rows)

    if len(lines) > MAX_CHART_ROWS:
        raise SyntaxProblem(
            number,
            f"{data_file.name} has {len(lines)} data rows after skip={spec.skip}; charts allow at most {MAX_CHART_ROWS}.",
        )
    rows: list[list[str]] = []
    values: list[Decimal] = []
    for row_number, line in enumerate(lines, start=spec.skip + 1):
        fields = line.split()
        if len(fields) != 2:
            raise SyntaxProblem(
                number,
                f"{data_file.name} data row {row_number} has {len(fields)} fields; "
                "chart rows need exactly a label and a number.",
            )
        rows.append(fields)
        values.append(_decimal(fields[1], data_file, row_number, number))
    if spec.kind == "bar" and any(value < 0 for value in values):
        raise SyntaxProblem(number, f"{data_file.name} contains a negative value; use a line chart because bars must start at zero.")
    caption = spec.caption + (" (one example run)" if data_file.suffix == ".example" else "")
    low, high = _chart_range(spec.kind, values)
    labels = json.dumps([row[0] for row in rows], ensure_ascii=False)
    numbers = "[" + ", ".join(row[1] for row in rows) + "]"
    return [
        "```mermaid",
        "xychart-beta",
        f"    accTitle: {caption}",
        f"    accDescr: {caption}. The x-axis is {spec.x_title}; the y-axis is {spec.y_title}.",
        f"    title {json.dumps(caption, ensure_ascii=False)}",
        f"    x-axis {json.dumps(spec.x_title, ensure_ascii=False)} {labels}",
        f"    y-axis {json.dumps(spec.y_title, ensure_ascii=False)} {_axis_number(low)} --> {_axis_number(high)}",
        f"    {spec.kind} {numbers}",
        "```",
        "",
        "<details>",
        "<summary>Data for this chart</summary>",
        "",
        *_markdown_table((spec.x_title, spec.y_title), rows, numeric_last=True),
        "",
        "</details>",
    ]


def listing_open(language: str, title: str) -> list[str]:
    label = f"Filename: {title}" if FILE_NAME.match(title) else title
    kind = "listing listing-output" if language == "text" else "listing"
    return [f'<figure class="{kind}">', f'<span class="file-name">{html.escape(label)}</span>', ""]


def callout_open(kind: str) -> list[str]:
    title, icon = CUSTOM_CALLOUTS[kind]
    return [
        f'<blockquote class="blockquote-tag blockquote-tag-{kind.lower()}">',
        f'<p class="blockquote-tag-title"><svg viewbox="0 0 16 16" width="18" height="18"><path d="{icon}"></path></svg>{title}</p>',
        "",
    ]


def convert(text: str, source_path: Path | None = None, repo_root: Path = REPO, *, expand_visuals: bool = True) -> str:
    """Rewrite one page of Markdown. Lines inside code fences are never changed."""
    out: list[str] = []
    fence: tuple[str, int] | None = None  # (fence character, length) while inside a code fence
    in_listing = False  # the current fence is wrapped in a <figure>
    in_callout = False  # inside the lines of a custom callout
    tabs_start = 0  # line of the open {{#tabs}}, or 0
    tab_start = 0  # line of the open {{#tab}}, or 0

    for number, line in enumerate(text.split("\n"), start=1):
        match = FENCE.match(line)
        if fence:
            out.append(line)
            if match and match.group(2)[0] == fence[0] and len(match.group(2)) >= fence[1] and not match.group(3):
                fence = None
                if in_listing:
                    out += ["", "</figure>"]
                    in_listing = False
            continue

        if in_callout:
            if line.startswith(">"):
                out.append(line[1:].removeprefix(" "))
                continue
            out += ["", "</blockquote>"]
            in_callout = False

        if match:
            fence = (match.group(2)[0], len(match.group(2)))
            titled = TITLED_INFO.match(match.group(3))
            if titled:
                out += listing_open(titled["language"], titled["title"])
                out.append(f"{match.group(1)}{match.group(2)}{titled['language']}")
                in_listing = True
            else:
                out.append(line)
            continue

        if VISUAL_DIRECTIVE.search(line) and not expand_visuals:
            out.append(line)
            continue
        visual = parse_visual_directive(line, number) if VISUAL_DIRECTIVE.search(line) else None
        if visual:
            if source_path is None:
                raise SyntaxProblem(number, "chart and table directives need the page path so their data file can be resolved.")
            out += render_visual_directive(visual, source_path, repo_root, number)
            continue

        callout = CALLOUT.match(line)
        if callout and callout["kind"].upper() in CUSTOM_CALLOUTS:
            out += callout_open(callout["kind"].upper())
            in_callout = True
            continue

        if TABS_OPEN.match(line):
            if tabs_start:
                raise SyntaxProblem(number, "{{#tabs}} inside another group of tabs; groups cannot be nested.")
            tabs_start = number
            out.append('<div class="tabs">')
            continue
        tab = TAB_OPEN.match(line)
        if tab:
            if not tabs_start:
                raise SyntaxProblem(number, "{{#tab ...}} outside {{#tabs}} ... {{#endtabs}}.")
            if tab_start:
                raise SyntaxProblem(number, f"{{{{#tab ...}}}} before the {{{{#endtab}}}} of the tab that starts on line {tab_start}.")
            tab_start = number
            label = html.escape(tab["label"])
            out += [f'<section class="tab" data-tab="{label}">', f'<p class="tab-label">{label}</p>', ""]
            continue
        if TAB_CLOSE.match(line):
            if not tab_start:
                raise SyntaxProblem(number, "{{#endtab}} without a {{#tab ...}} before it.")
            tab_start = 0
            out += ["", "</section>"]
            continue
        if TABS_CLOSE.match(line):
            if not tabs_start:
                raise SyntaxProblem(number, "{{#endtabs}} without a {{#tabs}} before it.")
            if tab_start:
                raise SyntaxProblem(number, f"{{{{#endtabs}}}} before the {{{{#endtab}}}} of the tab that starts on line {tab_start}.")
            tabs_start = 0
            out.append("</div>")
            continue

        out.append(line)

    if in_callout:
        out += ["", "</blockquote>"]
    if tabs_start:
        raise SyntaxProblem(tabs_start, "{{#tabs}} is never closed with {{#endtabs}}.")
    return "\n".join(out)


def convert_items(items: list, source_root: Path, repo_root: Path) -> None:
    for item in items:
        chapter = item.get("Chapter") if isinstance(item, dict) else None
        if not chapter:
            continue
        source = chapter.get("source_path")
        source_path = source_root / source if source else None
        try:
            chapter["content"] = convert(chapter["content"], source_path, repo_root)
        except SyntaxProblem as problem:
            sys.exit(f"docs/{chapter.get('source_path') or chapter['name']}:{problem.line}: {problem}")
        convert_items(chapter["sub_items"], source_root, repo_root)


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "supports":
        return 0  # every renderer gets the same Markdown
    context, book = json.load(sys.stdin)
    repo_root = Path(context["root"]).resolve()
    source_root = repo_root / context["config"]["book"].get("src", "src")
    convert_items(book["items"], source_root, repo_root)
    json.dump(book, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
