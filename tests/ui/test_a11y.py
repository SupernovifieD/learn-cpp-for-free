"""Accessibility checks: U5 (axe-core), U6 (headings) and U11 (keyboard focus).

axe-core is bundled inside the axe-playwright-python package. A violation that
comes from Material's own markup and cannot be fixed through configuration or
CSS may be listed in axe_allowlist.json as
    {"rule": "<axe rule id>", "selector": "<end of the node's selector>", "reason": "<why>"}
Every entry must also be reported in the milestone report. Anything that CAN be
fixed with configuration or CSS must be fixed instead of listed.
"""

import json
from pathlib import Path

import pytest
from conftest import AXE_WIDTHS, PAGES, SCHEMES, page_id

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


def _allowed(rule: str, target: str) -> bool:
    return any(entry["rule"] == rule and target.endswith(entry["selector"]) for entry in ALLOWLIST)


@pytest.mark.parametrize("path, width, scheme", A11Y_CASES)
def test_u5_no_serious_or_critical_axe_violations(tabs, path, width, scheme):
    """U5: axe-core finds no serious or critical problems (color contrast included)."""
    violations = tabs(width, scheme).survey(path).axe_violations
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


@pytest.mark.parametrize("path", PAGES, ids=[page_id(p) for p in PAGES])
def test_u6_one_h1_and_no_skipped_heading_levels(tabs, path):
    """U6: exactly one h1 per page, and headings never jump down by more than one level."""
    tab = tabs(1280, "light")
    tab.visit(path)
    h1_count = tab.page.evaluate("document.querySelectorAll('h1').length")
    assert h1_count == 1, f"The page has {h1_count} h1 elements; it must have exactly one."
    levels = tab.page.evaluate(
        "[...document.querySelectorAll('.md-content__inner :is(h1, h2, h3, h4, h5, h6)')]"
        ".map(h => [Number(h.tagName[1]), h.textContent.trim()])"
    )
    previous = 0
    for level, text in levels:
        assert level <= previous + 1, f"Heading level jumps from h{previous} to h{level} at '{text}'."
        previous = level


# ---------------------------------------------------------------- U11 ------

FOCUS_PAGES = ["", "conventions/"]

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
@pytest.mark.parametrize("path", FOCUS_PAGES, ids=[page_id(p) for p in FOCUS_PAGES])
def test_u11_first_tab_stop_is_the_visible_skip_link(tabs, path, width, scheme):
    """U11: on a fresh page the first Tab press lands on 'Skip to content', and it shows a focus outline."""
    tab = tabs(width, scheme)
    tab.visit(path)  # a fresh page load, not an in-page navigation
    tab.page.keyboard.press("Tab")
    first = tab.page.evaluate(DESCRIBE_FOCUS_JS)
    assert "md-skip" in first["cls"] and "Skip to content" in first["text"], (
        f"The first Tab stop is <{first['tag']} class='{first['cls']}'> '{first['text']}', not 'Skip to content'."
    )
    assert first["onScreen"], "The 'Skip to content' link has focus but cannot be seen."
    assert first["hasRing"], "The 'Skip to content' link has focus but no visible outline."


# Controls a reader uses with the keyboard, found by selector. A control that is not
# on screen at this width (for example the sidebar on a phone) is skipped.
FOCUS_CONTROLS = {
    "link in the text": ".md-content__inner p a:not(.headerlink)",
    "copy button": ".md-code__button",
    "collapsible question": ".md-content__inner summary",
    "repository link": "a.md-source",
    "sidebar link": ".md-sidebar--primary a.md-nav__link",
}
CONTROLS_REQUIRED_AT_ALL_WIDTHS = {"link in the text", "copy button", "collapsible question"}
SEARCH_FIELD_SHOWN_FROM = 960  # px; Material's 60em breakpoint


@pytest.mark.parametrize("scheme", SCHEMES)
@pytest.mark.parametrize("width", A11Y_WIDTHS)
def test_u11_focus_outlines_are_visible_on_the_controls_readers_use(tabs, width, scheme):
    """U11: keyboard focus is drawn on links, buttons, the palette toggle and the search box."""
    tab = tabs(width, scheme)
    tab.visit("conventions/")
    page = tab.page
    page.keyboard.press("Tab")  # keyboard mode, so programmatic focus draws a focus ring
    problems, checked = [], set()

    # Material's palette toggle: focus lands on a hidden radio button, and the ring is drawn on its visible label.
    for _ in range(6):
        if page.evaluate("document.activeElement.matches('input.md-option')"):
            break
        page.keyboard.press("Tab")
    ring = page.evaluate(
        """() => { const s = getComputedStyle(document.querySelector('[data-md-component="palette"] label:not([hidden])'));
                   return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0; }"""
    )
    checked.add("palette toggle")
    if not ring:
        problems.append("palette toggle: focus shows no outline")

    # Material's search box: the whole field changes color when it has focus (no outline is drawn).
    # Below 960px Material hides the field in an overlay that only the search icon opens, so there
    # is nothing on screen to check (see the keyboard notes in the milestone report).
    if width >= SEARCH_FIELD_SHOWN_FROM:
        before = page.evaluate("getComputedStyle(document.querySelector('.md-search__form')).backgroundColor")
        page.keyboard.press("Tab")
        assert page.evaluate("document.activeElement.matches('.md-search__input')"), "Tab after the palette toggle did not reach the search box."
        try:
            page.wait_for_function(
                "(before) => getComputedStyle(document.querySelector('.md-search__form')).backgroundColor !== before", arg=before, timeout=3000
            )
        except Exception:
            problems.append("search box: focus does not change how the field looks")
        checked.add("search box")

    # Everything else: focus it and look at its outline.
    for name, selector in FOCUS_CONTROLS.items():
        control = page.locator(selector).first
        if not control.is_visible():
            continue
        control.focus()
        stop = page.evaluate(DESCRIBE_FOCUS_JS)
        checked.add(name)
        if not stop["hasRing"]:
            problems.append(f"{name} (<{stop['tag']} class='{stop['cls']}'>): focus shows no outline")

    missing = CONTROLS_REQUIRED_AT_ALL_WIDTHS - checked
    assert not missing, f"These controls were not found on screen, so nothing was checked: {sorted(missing)}"
    if width >= 1280:
        assert {"repository link", "sidebar link"} <= checked, "The header repository link or the sidebar was not found at desktop width."
    assert not problems, "Focus is not visible on:\n" + "\n".join(f"  {p}" for p in problems)
