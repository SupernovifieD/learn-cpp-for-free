#!/usr/bin/env python3
"""Check the structure of every page in docs/ against the book's writing rules.

    python scripts/lint_content.py            # normal check (stubs allowed)
    python scripts/lint_content.py --final    # also forbid <!-- STUB --> markers and require lesson 0.11 to show the flags file

Rules, each reported as  docs/page.md:LINE: message
  * the page has front matter with a `description` of at most 160 characters
  * exactly one H1; for a page listed in the nav with a label it equals that label (the home page's H1
    is the site name instead); no skipped heading levels
  * no raw HTML (comments are fine)
  * a ```cpp fence is either one `--8<--` include line or at most 5 lines of code
  * images have alt text; links to other sites use https
  * none of: TODO, TBD, FIXME, lorem, "coming soon"
  * callouts use only the documented types, and tab labels only the documented sets
  * every file in examples/ is used by at least one page (.in files belong to the program next to them)
  * every page in docs/ is in the nav

Fenced code and `inline code` are never checked for HTML, links or forbidden words, because the book
legitimately shows such text there. The script needs Python 3 and PyYAML.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "docs"
EXAMPLES = REPO / "examples"
MAX_DESCRIPTION = 160
MAX_INLINE_CODE_LINES = 5
FLAGS_EXAMPLE = "examples/flags-gcc-clang.txt"
FLAGS_LESSON = "ch00-getting-started/11-warning-and-error-levels.md"

CALLOUT_TYPES = {"note", "tip", "warning", "danger", "question", "success", "best-practice", "key-insight", "advanced"}
TAB_SETS = [{"Windows", "macOS", "Linux"}, {"Visual Studio", "VS Code", "Command line"}]
FORBIDDEN_WORDS = re.compile(r"\b(TODO|TBD|FIXME|lorem|coming soon)\b", re.IGNORECASE)

FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*(.*)$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
INLINE_CODE = re.compile(r"(`+)(.+?)\1")
HTML_TAG = re.compile(r"<\s*/?\s*[A-Za-z][^<>]*>")
AUTOLINK = re.compile(r"<(https?|mailto):[^<>\s]*>")
IMAGE = re.compile(r"!\[([^\]]*)\]\(")
INSECURE_LINK = re.compile(r"(\]\(\s*|<)http://")
CALLOUT = re.compile(r"^\s*(?:!!!|\?\?\?\+?)\s+([\w-]+)")
TAB = re.compile(r'^(\s*)===\+?\s+"([^"]*)"')


class _TolerantLoader(yaml.SafeLoader):
    """Reads mkdocs.yml although it contains Python-specific tags such as !!python/name:..."""


_TolerantLoader.add_multi_constructor("tag:yaml.org,2002:python/name:", lambda loader, suffix, node: None)


@dataclass
class Problem:
    page: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.page}:{self.line}: {self.message}" if self.line else f"{self.page}: {self.message}"


def read_nav(config: dict) -> dict[str, str | None]:
    """Map each page in the nav (path relative to docs/) to its label, or None when it has none.

    A chapter's index page is listed without a label, so it takes its chapter's label.
    """
    pages: dict[str, str | None] = {}

    def walk(items: list, chapter: str | None = None) -> None:
        for item in items:
            if isinstance(item, str):
                pages[item] = chapter
                continue
            for label, value in item.items():
                if isinstance(value, str):
                    pages[value] = label
                else:
                    walk(value, label)

    walk(config.get("nav", []))
    return pages


def strip_inline_code(line: str) -> str:
    return INLINE_CODE.sub("", line)


def split_front_matter(text: str) -> tuple[dict | None, int]:
    """Return (front matter as a dict or None, number of lines it occupies)."""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for end in range(1, len(lines)):
            if lines[end].strip() == "---":
                try:
                    data = yaml.safe_load("\n".join(lines[1:end]))
                except yaml.YAMLError:
                    return None, end + 1
                return (data if isinstance(data, dict) else None), end + 1
    return None, 0


def lint_page(path: Path, label: str | None, site_name: str, final: bool) -> tuple[list[Problem], set[str]]:
    """Lint one page. Returns its problems and the set of example files it includes."""
    rel = path.relative_to(DOCS).as_posix()
    shown = path.relative_to(REPO).as_posix()
    problems: list[Problem] = []

    def add(line: int, message: str) -> None:
        problems.append(Problem(shown, line, message))

    text = path.read_text()
    front, front_lines = split_front_matter(text)
    if front is None or not isinstance(front.get("description"), str) or not front["description"].strip():
        add(1, "front matter must contain a non-empty `description:` (one sentence, at most 160 characters).")
    elif len(front["description"]) > MAX_DESCRIPTION:
        add(1, f"`description` is {len(front['description'])} characters; the limit is {MAX_DESCRIPTION}.")

    headings: list[tuple[int, int, str]] = []  # (line, level, text)
    included: set[str] = set()
    in_fence = False
    fence_char, fence_len, fence_info, fence_start, fence_body = "", 0, "", 0, []
    in_comment = False
    previous_tab_group: tuple[int, set[str], int] | None = None  # (indent, labels so far, first line)

    for number, raw in enumerate(text.split("\n"), start=1):
        if number <= front_lines:
            continue
        line = raw
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
                    is_include = len(body) == 1 and body[0].strip().startswith("--8<--")
                    if not is_include and len(body) > MAX_INLINE_CODE_LINES:
                        add(fence_start, f"a cpp fence has {len(body)} lines; complete programs must be included from examples/ "
                                         f'(--8<-- "examples/...") and inline fragments may have at most {MAX_INLINE_CODE_LINES} lines.')
                for code_line in body:
                    match = re.search(r'--8<--\s+"([^"]+)"', code_line)
                    if match:
                        included.add(match.group(1))
            else:
                fence_body.append(line)
            continue
        if fence:
            in_fence, fence_char, fence_len, fence_info, fence_start, fence_body = True, fence.group(2)[0], len(fence.group(2)), fence.group(3), number, []
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

        # includes on their own line (outside a fence) count as references too
        for match in re.finditer(r'--8<--\s+"([^"]+)"', line):
            included.add(match.group(1))

        heading = HEADING.match(line)
        if heading:
            title = re.sub(r"\s*\{[^}]*\}\s*$", "", heading.group(2)).strip()
            headings.append((number, len(heading.group(1)), title))

        prose = strip_inline_code(line)
        if prose.strip().startswith("--8<--"):
            continue
        without_autolinks = AUTOLINK.sub("", prose)
        tag = HTML_TAG.search(without_autolinks)
        if tag:
            add(number, f"raw HTML is not allowed in pages: {tag.group(0)!r} (put code in backticks, or use Markdown).")
        for image in IMAGE.finditer(prose):
            if not image.group(1).strip():
                add(number, "image without alt text.")
        if INSECURE_LINK.search(prose):
            add(number, "link to another site must use https.")
        found = FORBIDDEN_WORDS.search(prose)
        if found:
            add(number, f"forbidden word '{found.group(0)}'.")

        callout = CALLOUT.match(line)
        if callout and callout.group(1) not in CALLOUT_TYPES:
            add(number, f"unknown callout type '{callout.group(1)}'; use one of {', '.join(sorted(CALLOUT_TYPES))}.")

        tab = TAB.match(line)
        if not tab and previous_tab_group and line.strip() and len(line) - len(line.lstrip()) <= previous_tab_group[0]:
            previous_tab_group = None  # text outside the tabs: the group of tabs is over
        if tab:
            indent, name = len(tab.group(1)), tab.group(2)
            labels = previous_tab_group[1] if previous_tab_group and previous_tab_group[0] == indent else set()
            labels.add(name)
            previous_tab_group = (indent, labels, number)
            if not any(name in label_set for label_set in TAB_SETS):
                add(number, f"tab label '{name}' is not allowed; use exactly Windows | macOS | Linux or Visual Studio | VS Code | Command line.")
            elif not any(labels <= label_set for label_set in TAB_SETS):
                add(number, f"tab '{name}' mixes label sets in one group of tabs; use one set per group.")

    if in_fence:
        add(fence_start, "a code fence is never closed.")

    # headings
    h1s = [h for h in headings if h[1] == 1]
    if len(h1s) != 1:
        add(h1s[1][0] if len(h1s) > 1 else 1, f"a page needs exactly one H1, found {len(h1s)}.")
    elif rel == "index.md":
        if h1s[0][2] != site_name:
            add(h1s[0][0], f"the home page H1 must be the site name '{site_name}', not '{h1s[0][2]}'.")
    elif label is not None and h1s[0][2] != label:
        add(h1s[0][0], f"H1 '{h1s[0][2]}' must equal its nav label '{label}'.")
    previous = 0
    for number, level, title in headings:
        if level > previous + 1:
            add(number, f"heading level jumps from H{previous or 'none'} to H{level} at '{title}'; do not skip levels.")
        previous = level
    return problems, included


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
                problems.append(Problem(rel, 0, f"must be included in {FLAGS_LESSON} (--8<-- \"{rel}\")."))
            continue
        if rel not in used:
            problems.append(Problem(rel, 0, 'is not used by any page; include it with --8<-- "' + rel + '" or delete it.'))
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the structure and writing rules of docs/.")
    parser.add_argument("--final", action="store_true", help="also forbid <!-- STUB --> markers and require lesson 0.11 to include the flags file")
    args = parser.parse_args()

    config = yaml.load((REPO / "mkdocs.yml").read_text(), Loader=_TolerantLoader)
    nav = read_nav(config)
    site_name = config["site_name"]
    pages = sorted(DOCS.rglob("*.md"))
    problems: list[Problem] = []
    included_by_page: dict[str, set[str]] = {}

    for page in pages:
        rel = page.relative_to(DOCS).as_posix()
        if rel not in nav:
            problems.append(Problem(page.relative_to(REPO).as_posix(), 0, "page is not listed in the nav in mkdocs.yml."))
        page_problems, included = lint_page(page, nav.get(rel), site_name, args.final)
        problems += page_problems
        included_by_page[rel] = included
    for rel in nav:
        if not (DOCS / rel).exists():
            problems.append(Problem("mkdocs.yml", 0, f"nav lists {rel}, which does not exist."))
    problems += lint_examples_used(included_by_page, args.final)

    for problem in problems:
        print(problem)
    mode = "final" if args.final else "normal"
    print(f"\nChecked {len(pages)} pages ({mode} mode): " + (f"{len(problems)} problem(s)." if problems else "no problems."))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
