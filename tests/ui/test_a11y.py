"""Accessibility checks: U5 (axe-core), U6 (headings) and U11 (keyboard focus).

axe-core is bundled inside the axe-playwright-python package. A violation that
comes from mdBook's own markup and cannot be fixed through configuration, CSS
or the book's small script may be listed in axe_allowlist.json as
    {"rule": "<axe rule id>", "selector": "<end of the node's selector>", "reason": "<why>"}
Anything that CAN be fixed must be fixed instead of listed.
"""

import json
from pathlib import Path

import pytest
from conftest import AXE_WIDTHS, CONTENT, DETAILS_PAGES, PAGES, SCHEMES, SIDEBAR_SHOWN_FROM, page_id

A11Y_WIDTHS = AXE_WIDTHS
BLOCKING_IMPACTS = {"serious", "critical"}
ALLOWLIST = json.loads((Path(__file__).parent / "axe_allowlist.json").read_text())

# Run on the same worker as the layout checks of that width and scheme, so one page load serves both.
A11Y_CASES = [
    pytest.param(path, width, scheme, id=f"{page_id(path)}-{width}-{scheme}")
    for scheme in SCHEMES
    for width in A11Y_WIDTHS
    for path in PAGES
]


# The same axe-core check with every <details> opened, for the pages that have questions: the colors and
# structure of the answers are never rendered while they are closed.
OPENED_A11Y_CASES = [
    pytest.param(path, width, scheme, id=f"{page_id(path)}-open-{width}-{scheme}")
    for scheme in SCHEMES
    for width in A11Y_WIDTHS
    for path in DETAILS_PAGES
]


def _allowed(rule: str, target: str) -> bool:
    return any(entry["rule"] == rule and target.endswith(entry["selector"]) for entry in ALLOWLIST)


def _assert_no_blocking_violations(violations, width):
    assert violations is not None, f"axe-core did not run at {width}px, but U5 requires it."
    lines = []
    for violation in violations:
        if violation["impact"] not in BLOCKING_IMPACTS:
            continue
        for node in violation["nodes"]:
            target = ", ".join(str(t) for t in node["target"])
            if not _allowed(violation["id"], target):
                summary = " ".join(node.get("failureSummary", "").split("\n")[1:2]).strip()
                lines.append(f"  [{violation['impact']}] {violation['id']}: {violation['help']}\n      at {target}\n      {summary}")
    assert not lines, "axe-core found problems:\n" + "\n".join(lines)


@pytest.mark.parametrize("path, width, scheme", A11Y_CASES)
def test_u5_no_serious_or_critical_axe_violations(tabs, path, width, scheme):
    """U5: axe-core finds no serious or critical problems (color contrast included)."""
    _assert_no_blocking_violations(tabs(width, scheme).survey(path).axe_violations, width)


@pytest.mark.parametrize("path, width, scheme", OPENED_A11Y_CASES)
def test_u5_no_serious_or_critical_axe_violations_with_every_answer_opened(tabs, path, width, scheme):
    """U5 with every answer opened: axe-core also finds nothing in the questions and answers."""
    _assert_no_blocking_violations(tabs(width, scheme).survey(path, open_details=True).axe_violations, width)


@pytest.mark.parametrize("path", PAGES, ids=[page_id(p) for p in PAGES])
def test_u6_one_h1_and_no_skipped_heading_levels(tabs, path):
    """U6: the page's content has exactly one h1, and headings never jump down by more than one level.

    mdBook also puts the book title in an h1 in its menu bar on every page; that one belongs to
    the frame, not to the page, so only the content is counted.
    """
    tab = tabs(1280, "light")
    tab.visit(path)
    levels = tab.page.evaluate(
        f"[...document.querySelectorAll('{CONTENT} :is(h1, h2, h3, h4, h5, h6)')]"
        ".map(h => [Number(h.tagName[1]), h.textContent.trim()])"
    )
    h1_count = sum(1 for level, _ in levels if level == 1)
    assert h1_count == 1, f"The page's content has {h1_count} h1 elements; it must have exactly one."
    previous = 0
    for level, text in levels:
        assert level <= previous + 1, f"Heading level jumps from h{previous} to h{level} at '{text}'."
        previous = level


# ---------------------------------------------------------------- U11 ------

DESCRIBE_FOCUS_JS = """() => {
  const el = document.activeElement;
  const style = getComputedStyle(el);
  const rect = el.getBoundingClientRect();
  return { tag: el.tagName.toLowerCase(), cls: el.className.toString(), id: el.id,
           text: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 40),
           hasRing: (style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) > 0) || style.boxShadow !== 'none',
           onScreen: rect.width > 1 && rect.height > 1 && rect.top >= 0 && rect.left >= 0 && rect.right <= innerWidth };
}"""


@pytest.mark.parametrize("scheme", SCHEMES)
@pytest.mark.parametrize("width", A11Y_WIDTHS)
def test_u11_the_tab_key_reaches_visible_controls_with_a_focus_outline(tabs, width, scheme):
    """U11: pressing Tab on a fresh page moves through controls that are on screen and show where focus is."""
    tab = tabs(width, scheme)
    tab.visit("index.html")
    for step in range(1, 6):
        tab.page.keyboard.press("Tab")
        stop = tab.page.evaluate(DESCRIBE_FOCUS_JS)
        where = f"Tab stop {step} (<{stop['tag']} id='{stop['id']}' class='{stop['cls']}'> '{stop['text']}')"
        assert stop["tag"] != "body", f"Tab stop {step} did not focus anything."
        assert stop["onScreen"], f"{where} has focus but cannot be seen."
        assert stop["hasRing"], f"{where} has focus but no visible outline."


# Controls a reader uses with the keyboard, found by selector. A control that is not
# on screen at this width (for example the sidebar on a phone) is skipped.
FOCUS_CONTROLS = {
    "link in the text": f"{CONTENT} p a",
    "copy button": f"{CONTENT} pre .clip-button",
    "collapsible question": f"{CONTENT} summary",
    "tab": f"{CONTENT} [role=tab]",
    "theme button": "#mdbook-theme-toggle",
    "search button": "#mdbook-search-toggle",
    "sidebar button": "#mdbook-sidebar-toggle",
    "repository link": ".right-buttons a[title='Git repository']",
    "edit link": ".right-buttons a[rel=edit]",
    "next page link": "a.nav-chapters.next, a.mobile-nav-chapters.next",
    "sidebar link": "#mdbook-sidebar .chapter a",
}
CONTROLS_REQUIRED_AT_ALL_WIDTHS = set(FOCUS_CONTROLS) - {"sidebar link"}


@pytest.mark.parametrize("scheme", SCHEMES)
@pytest.mark.parametrize("width", A11Y_WIDTHS)
def test_u11_focus_outlines_are_visible_on_the_controls_readers_use(tabs, width, scheme):
    """U11: keyboard focus is drawn on links, buttons, tabs, questions and the search box."""
    tab = tabs(width, scheme)
    tab.visit("conventions.html")
    page = tab.page
    page.keyboard.press("Tab")  # keyboard mode, so programmatic focus draws a focus ring
    problems, checked = [], set()

    sidebar_open = page.evaluate("document.documentElement.classList.contains('sidebar-visible')")
    for name, selector in FOCUS_CONTROLS.items():
        if name == "sidebar link" and not sidebar_open:
            continue  # the closed sidebar is off screen, and its links are not Tab stops
        if name == "copy button":
            page.locator(f"{CONTENT} pre").first.hover()  # mdBook shows the button while the pointer is on the block
            try:
                page.locator(selector).first.wait_for(state="visible", timeout=5_000)  # it fades in, so wait for it
            except Exception:
                pass  # reported below as a control that was not found
        control = page.locator(selector).locator("visible=true").first
        if control.count() == 0:
            continue
        control.focus()
        stop = page.evaluate(DESCRIBE_FOCUS_JS)
        checked.add(name)
        if not stop["hasRing"]:
            problems.append(f"{name} (<{stop['tag']} class='{stop['cls']}'>): focus shows no outline")

    # The search box appears when the search button is used, and takes focus itself.
    page.evaluate("window.scrollTo(0, 0)")  # mdBook tucks its menu bar away while the reader scrolls down
    page.locator("#mdbook-search-toggle").click()
    page.wait_for_function("document.activeElement.id === 'mdbook-searchbar'", timeout=5_000)
    stop = page.evaluate(DESCRIBE_FOCUS_JS)
    checked.add("search box")
    if not stop["hasRing"]:
        problems.append("search box: focus shows no outline")
    page.keyboard.press("Escape")

    missing = CONTROLS_REQUIRED_AT_ALL_WIDTHS - checked
    assert not missing, f"These controls were not found on screen, so nothing was checked: {sorted(missing)}"
    if width >= SIDEBAR_SHOWN_FROM:
        assert "sidebar link" in checked, "The sidebar was not found at desktop width."
    assert not problems, "Focus is not visible on:\n" + "\n".join(f"  {p}" for p in problems)
