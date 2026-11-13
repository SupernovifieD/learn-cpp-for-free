#!/usr/bin/env python3
"""Check the structure of every page in docs/ against the book's writing rules.

    python scripts/lint_content.py            # normal check (stubs allowed)
    python scripts/lint_content.py --final    # also forbid <!-- STUB --> markers and require lesson 0.11 to show the flags file

Rules, each reported as  docs/page.md:LINE: message
  * docs/SUMMARY.md lists every page exactly once, and every page it lists exists
  * exactly one H1, equal to the page's label in SUMMARY.md (the home page's H1 is the book title
    from book.toml instead); no skipped heading levels
  * no front matter, and none of the syntax of the book's former site generator
  * no raw HTML except <details>, <summary> and <kbd> (comments are fine)
  * a code fence has a language and at most a title="..."; a ```cpp fence is either one
    {{#include ...}} line or at most 5 lines of code
  * every {{#include ...}} names a file that exists
  * links to other pages point at a listed page and, with a #fragment, at one of its headings
  * images have alt text; links to other sites use https
  * none of: TODO, TBD, FIXME, lorem, "coming soon"
  * no text left over from templates/lesson.md or templates/chapter-index.md (their instructions and placeholders)
  * callouts use only the documented kinds, and tabs are well formed and use only the documented label sets
  * every file in examples/ is used by at least one page (.in files belong to the program next to them)

Fenced code and `inline code` are never checked for HTML, links or forbidden words, because the book
legitimately shows such text there. The script needs only Python 3.11 or newer.
"""

from __future__ import annotations

import argparse
import posixpath
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

from mdbook_cppbook import CALLOUT, CUSTOM_CALLOUTS, FENCE, NATIVE_CALLOUTS, TAB_OPEN, TABS_CLOSE, TABS_OPEN, TITLED_INFO, SyntaxProblem, convert

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "docs"
EXAMPLES = REPO / "examples"
SUMMARY = "SUMMARY.md"
MAX_INLINE_CODE_LINES = 5
FLAGS_EXAMPLE = "examples/flags-gcc-clang.txt"
FLAGS_LESSON = "ch00-getting-started/11-warning-and-error-levels.md"

CALLOUT_KINDS = NATIVE_CALLOUTS | set(CUSTOM_CALLOUTS)
TAB_SETS = [{"Windows", "macOS", "Linux"}, {"Visual Studio", "VS Code", "Command line"}]
ALLOWED_HTML = {"<details>", "</details>", "<summary>", "</summary>", "<kbd>", "</kbd>"}
# Text that only exists in templates/lesson.md and templates/chapter-index.md. Finding it in a page
# means the template was not filled in (HTML comments are published in the page source, too).
TEMPLATE_LEFTOVERS = [
    "HOW TO USE THIS TEMPLATE",
    "Title of the lesson",
    "Title of a primary source",
    "Say in two to four sentences",
    "First main point.",
    "# 1. Chapter title",
    "Explain the first big idea of the chapter",
]
FORBIDDEN_WORDS = re.compile(r"\b(TODO|TBD|FIXME|lorem|coming soon)\b", re.IGNORECASE)
# Syntax of the former site generator. mdBook would print it as plain text.
OBSOLETE_SYNTAX = [
    (re.compile(r"^\s*(!!!|\?\?\?\+?)\s"), "write callouts as `> [!NOTE]` block quotes and questions as <details>"),
    (re.compile(r'^\s*===\+?\s+"'), "write tabs with {{#tabs}} and {{#tab Label}}"),
    (re.compile(r"\+\+[a-z0-9]+(\+[a-z0-9]+)*\+\+"), "write keys as <kbd>Ctrl</kbd>+<kbd>F5</kbd>"),
    (re.compile(r"--8<--"), "include files with {{#include ...}}"),
    (re.compile(r"\)\{\s*[.#][^}]*\}"), "attribute lists such as { .class } are not supported"),
]

SUMMARY_ENTRY = re.compile(r"^\s*(?:[-*]\s+)?\[(?P<label>[^\]]+)\]\((?P<path>[^)]*)\)\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
INLINE_CODE = re.compile(r"(`+)(.+?)\1")
HTML_TAG = re.compile(r"<\s*/?\s*[A-Za-z][^<>]*>")
AUTOLINK = re.compile(r"<(https?|mailto):[^<>\s]*>")
IMAGE = re.compile(r"!\[([^\]]*)\]\(")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(\s*([^)\s]+)[^)]*\)")
INSECURE_LINK = re.compile(r"(\]\(\s*|<)http://")
INCLUDE = re.compile(r"\{\{#include\s+([^}\s]+)\s*\}\}")
ANY_CALLOUT = re.compile(r"^>\s*\[!(?P<kind>[^\]]*)\]")


@dataclass
class Problem:
    page: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.page}:{self.line}: {self.message}" if self.line else f"{self.page}: {self.message}"


def read_summary() -> tuple[dict[str, str], list[Problem]]:
    """Map each page in docs/SUMMARY.md (path relative to docs/) to its label, in reading order."""
    shown = f"docs/{SUMMARY}"
    pages: dict[str, str] = {}
    problems: list[Problem] = []
    for number, line in enumerate((DOCS / SUMMARY).read_text().split("\n"), start=1):
        if not line.strip() or line.startswith("#") or line.strip() == "---":
            continue
        entry = SUMMARY_ENTRY.match(line)
        if not entry or not entry["path"]:
            problems.append(Problem(shown, number, "every line must be a link to a page, such as `- [0.1 Title](chapter/01-title.md)`."))
            continue
        path = entry["path"]
        if path in pages:
            problems.append(Problem(shown, number, f"{path} is listed twice."))
        elif not (DOCS / path).is_file():
            problems.append(Problem(shown, number, f"{path} does not exist."))
        pages[path] = entry["label"]
    return pages, problems


def heading_id(title: str) -> str:
    """The id that mdBook gives a heading: lower case, spaces to hyphens, punctuation dropped."""
    plain = re.sub(r"[`*]", "", title).strip().lower()
    return "".join("-" if ch.isspace() else ch for ch in plain if ch.isalnum() or ch.isspace() or ch in "_-")


def strip_inline_code(line: str) -> str:
    return INLINE_CODE.sub("", line)


@dataclass
class Page:
    problems: list[Problem]
    included: set[str]  # files it includes, relative to the repository
    links: list[tuple[int, str]]  # (line, target) of links to other pages
    anchors: set[str]  # ids of its headings


def lint_page(path: Path, label: str | None, book_title: str, final: bool) -> Page:
    rel = path.relative_to(DOCS).as_posix()
    shown = path.relative_to(REPO).as_posix()
    problems: list[Problem] = []

    def add(line: int, message: str) -> None:
        problems.append(Problem(shown, line, message))

    text = path.read_text()
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        add(1, "front matter is not supported: start the page with its H1.")

    for leftover in TEMPLATE_LEFTOVERS:
        position = text.find(leftover)
        if position != -1:
            add(text.count("\n", 0, position) + 1, f"text from the lesson or chapter template is still here ('{leftover}'): replace the placeholders and delete the template's comments.")

    try:
        convert(text)
    except SyntaxProblem as problem:
        add(problem.line, str(problem))

    headings: list[tuple[int, int, str]] = []  # (line, level, text)
    included: set[str] = set()
    links: list[tuple[int, str]] = []
    in_fence = False
    fence_char, fence_len, fence_info, fence_start, fence_body = "", 0, "", 0, []
    in_comment = False
    tab_labels: set[str] = set()

    def note_includes(number: int, line: str) -> None:
        for match in INCLUDE.finditer(line):
            target = (path.parent / match.group(1).split(":")[0]).resolve()
            if not target.is_file():
                add(number, f"{{{{#include {match.group(1)}}}}} names a file that does not exist (the path is relative to this page).")
            elif REPO in target.parents:
                included.add(target.relative_to(REPO).as_posix())

    for number, line in enumerate(lines, start=1):
        fence = FENCE.match(line)
        if in_fence:
            if fence and fence.group(2)[0] == fence_char and len(fence.group(2)) >= fence_len and not fence.group(3):
                in_fence = False
                language = fence_info.split()[0].lower() if fence_info.split() else ""
                body = list(fence_body)
                while body and not body[0].strip():
                    body.pop(0)
                while body and not body[-1].strip():
                    body.pop()
                if language in {"cpp", "c++", "cxx"}:
                    is_include = len(body) == 1 and INCLUDE.fullmatch(body[0].strip())
                    if not is_include and len(body) > MAX_INLINE_CODE_LINES:
                        add(fence_start, f"a cpp fence has {len(body)} lines; complete programs must be included from examples/ "
                                         f"({{{{#include ../../examples/...}}}}) and inline fragments may have at most {MAX_INLINE_CODE_LINES} lines.")
            else:
                fence_body.append(line)
                note_includes(number, line)
            continue
        if fence:
            in_fence, fence_char, fence_len, fence_info, fence_start, fence_body = True, fence.group(2)[0], len(fence.group(2)), fence.group(3), number, []
            if not fence_info:
                add(number, "a code fence needs a language, such as ```cpp, ```bash or ```text.")
            elif not re.fullmatch(r"[\w+-]+", fence_info) and not TITLED_INFO.match(fence_info):
                add(number, f'a code fence may only have a language and a title, such as ```cpp title="hello-world.cpp" (found {fence_info!r}).')
            continue

        # HTML comments: allowed, except the stub marker in the final check.
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line:
            if "STUB" in line and final:
                add(number, "the <!-- STUB --> marker must be removed from a finished lesson.")
            comment_text = line
            if "-->" not in line[line.index("<!--") :]:
                in_comment = True
            line = re.sub(r"<!--.*?(-->|$)", "", comment_text)
            if FORBIDDEN_WORDS.search(comment_text):
                add(number, f"forbidden word '{FORBIDDEN_WORDS.search(comment_text).group(0)}' (also not allowed in comments).")

        note_includes(number, line)

        heading = HEADING.match(line)
        if heading:
            headings.append((number, len(heading.group(1)), heading.group(2).strip()))

        prose = strip_inline_code(line)
        for pattern, advice in OBSOLETE_SYNTAX:
            if pattern.search(prose):
                add(number, f"syntax that mdBook does not support: {advice}.")
        for tag in HTML_TAG.finditer(AUTOLINK.sub("", prose)):
            if tag.group(0) not in ALLOWED_HTML:
                add(number, f"raw HTML is not allowed in pages: {tag.group(0)!r} (only <details>, <summary> and <kbd>, without attributes).")
        for image in IMAGE.finditer(prose):
            if not image.group(1).strip():
                add(number, "image without alt text.")
        if INSECURE_LINK.search(prose):
            add(number, "link to another site must use https.")
        found = FORBIDDEN_WORDS.search(prose)
        if found:
            add(number, f"forbidden word '{found.group(0)}'.")
        for link in LINK.finditer(prose):
            target = link.group(1)
            if not re.match(r"[a-z][a-z0-9+.-]*:", target):
                links.append((number, target))

        callout = ANY_CALLOUT.match(line)
        if callout and not (CALLOUT.match(line) and callout["kind"] in CALLOUT_KINDS):
            add(number, f"unknown callout '[!{callout['kind']}]'; write one of {', '.join(sorted(CALLOUT_KINDS))} in capitals, alone on its line.")

        if TABS_OPEN.match(line):
            tab_labels = set()
        elif TABS_CLOSE.match(line) and len(tab_labels) < 2:
            add(number, "a group of tabs needs at least two tabs.")
        elif line.startswith("{{#tab ") or line.startswith("{{#tab}"):
            tab = TAB_OPEN.match(line)
            name = tab["label"] if tab else ""
            tab_labels.add(name)
            if not any(name in label_set for label_set in TAB_SETS):
                add(number, f"tab label '{name}' is not allowed; use exactly Windows | macOS | Linux or Visual Studio | VS Code | Command line.")
            elif not any(tab_labels <= label_set for label_set in TAB_SETS):
                add(number, f"tab '{name}' mixes label sets in one group of tabs; use one set per group.")
        elif re.match(r"\s+\{\{#(tabs|tab|endtab|endtabs)\b", line):
            add(number, "tab markers must start at the beginning of the line.")

    if in_fence:
        add(fence_start, "a code fence is never closed.")

    # headings
    h1s = [h for h in headings if h[1] == 1]
    if len(h1s) != 1:
        add(h1s[1][0] if len(h1s) > 1 else 1, f"a page needs exactly one H1, found {len(h1s)}.")
    elif rel == "index.md":
        if h1s[0][2] != book_title:
            add(h1s[0][0], f"the home page H1 must be the book title '{book_title}', not '{h1s[0][2]}'.")
    elif label is not None and h1s[0][2] != label:
        add(h1s[0][0], f"H1 '{h1s[0][2]}' must equal its label in {SUMMARY}, '{label}'.")
    previous = 0
    for number, level, title in headings:
        if level > previous + 1:
            add(number, f"heading level jumps from H{previous or 'none'} to H{level} at '{title}'; do not skip levels.")
        previous = level
    return Page(problems, included, links, {heading_id(title) for _, _, title in headings})


def lint_links(pages: dict[str, Page], listed: dict[str, str]) -> list[Problem]:
    """Links between pages must lead to a listed page, and a #fragment to one of its headings."""
    problems = []
    for rel, page in pages.items():
        for line, target in page.links:
            file, _, fragment = target.partition("#")
            other = posixpath.normpath(posixpath.join(posixpath.dirname(rel), file)) if file else rel
            shown = f"docs/{rel}"
            if file and not file.endswith(".md"):
                problems.append(Problem(shown, line, f"link '{target}' must point at a Markdown page (a path that ends in .md)."))
            elif other not in listed or other not in pages:
                problems.append(Problem(shown, line, f"link '{target}' leads to docs/{other}, which is not a page of the book."))
            elif fragment and fragment not in pages[other].anchors:
                problems.append(Problem(shown, line, f"link '{target}': docs/{other} has no heading with the id '{fragment}'."))
    return problems


def lint_examples_used(included_by_page: dict[str, set[str]], final: bool) -> list[Problem]:
    """Every file in examples/ must be shown by at least one page."""
    used = {path for paths in included_by_page.values() for path in paths}
    problems = []
    for file in sorted(p for p in EXAMPLES.rglob("*") if p.is_file()):
        rel = file.relative_to(REPO).as_posix()
        if file.suffix == ".in":
            program = file.with_suffix(".cpp")
            if not program.exists():
                problems.append(Problem(rel, 0, "input file has no program next to it."))
            continue
        if rel == FLAGS_EXAMPLE:
            if not final:
                continue  # lesson 0.11 includes it; enforced when everything else is finished
            lesson = DOCS / FLAGS_LESSON
            if not lesson.exists() or rel not in included_by_page.get(FLAGS_LESSON, set()):
                problems.append(Problem(rel, 0, f"must be included in {FLAGS_LESSON} with {{{{#include ...}}}}."))
            continue
        if rel not in used:
            problems.append(Problem(rel, 0, "is not used by any page; include it with {{#include ...}} or delete it."))
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the structure and writing rules of docs/.")
    parser.add_argument("--final", action="store_true", help="also forbid <!-- STUB --> markers and require lesson 0.11 to include the flags file")
    args = parser.parse_args()

    config = tomllib.loads((REPO / "book.toml").read_text())
    book_title = config["book"]["title"]
    listed, problems = read_summary()
    files = sorted(page for page in DOCS.rglob("*.md") if page.relative_to(DOCS).as_posix() != SUMMARY)
    pages: dict[str, Page] = {}

    for file in files:
        rel = file.relative_to(DOCS).as_posix()
        if rel not in listed:
            problems.append(Problem(file.relative_to(REPO).as_posix(), 0, f"page is not listed in docs/{SUMMARY}."))
        pages[rel] = lint_page(file, listed.get(rel), book_title, args.final)
        problems += pages[rel].problems
    problems += lint_links(pages, listed)
    problems += lint_examples_used({rel: page.included for rel, page in pages.items()}, args.final)

    for problem in problems:
        print(problem)
    mode = "final" if args.final else "normal"
    print(f"\nChecked {len(files)} pages ({mode} mode): " + (f"{len(problems)} problem(s)." if problems else "no problems."))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
