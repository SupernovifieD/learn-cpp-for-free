#!/usr/bin/env python3
"""mdBook preprocessor for the three pieces of lesson syntax that mdBook does not have itself.

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

scripts/lint_content.py imports the patterns below, so the linter and the build agree on the syntax.
"""

from __future__ import annotations

import html
import json
import re
import sys

FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*(.*)$")
TITLED_INFO = re.compile(r'^(?P<language>[\w+-]+)\s+title="(?P<title>[^"]*)"\s*$')
FILE_NAME = re.compile(r"^[\w.-]+\.[A-Za-z0-9]+$")
CALLOUT = re.compile(r"^>\s*\[!(?P<kind>[A-Za-z-]+)\]\s*$")
TABS_OPEN = re.compile(r"^\{\{#tabs\}\}\s*$")
TABS_CLOSE = re.compile(r"^\{\{#endtabs\}\}\s*$")
TAB_OPEN = re.compile(r"^\{\{#tab\s+(?P<label>[^{}]+?)\s*\}\}\s*$")
TAB_CLOSE = re.compile(r"^\{\{#endtab\}\}\s*$")

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
    """A mistake in the tab markers. The build stops and shows the page and line."""

    def __init__(self, line: int, message: str) -> None:
        super().__init__(message)
        self.line = line


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


def convert(text: str) -> str:
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


def convert_items(items: list) -> None:
    for item in items:
        chapter = item.get("Chapter") if isinstance(item, dict) else None
        if not chapter:
            continue
        try:
            chapter["content"] = convert(chapter["content"])
        except SyntaxProblem as problem:
            sys.exit(f"docs/{chapter.get('source_path') or chapter['name']}:{problem.line}: {problem}")
        convert_items(chapter["sub_items"])


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "supports":
        return 0  # every renderer gets the same Markdown
    _context, book = json.load(sys.stdin)
    convert_items(book["items"])
    json.dump(book, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
