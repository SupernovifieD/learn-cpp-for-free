"""Layout checks U1-U4: every page, at every viewport width, in both color schemes.

Each (page, width, scheme) is loaded once and measured once (see Tab.survey in
conftest.py); the four tests below only read that measurement.
"""

import pytest
from conftest import PAGES, SCHEMES, WIDTHS, page_id

# Tests with the same xdist_group run on the same worker (make test-ui uses --dist loadgroup),
# so each page is loaded once per width and scheme and reused by all four checks.
LAYOUT_CASES = [
    pytest.param(path, width, scheme, id=f"{page_id(path)}-{width}-{scheme}", marks=pytest.mark.xdist_group(f"layout-{width}-{scheme}"))
    for scheme in SCHEMES
    for width in WIDTHS
    for path in PAGES
]


@pytest.mark.parametrize("path, width, scheme", LAYOUT_CASES)
def test_u1_no_horizontal_page_scroll(tabs, path, width, scheme):
    """U1: the page is never wider than the window."""
    survey = tabs(width, scheme).survey(path)
    assert survey.scroll_width <= survey.client_width, (
        f"The page scrolls sideways: it is {survey.scroll_width}px wide in a {survey.client_width}px window."
    )


@pytest.mark.parametrize("path, width, scheme", LAYOUT_CASES)
def test_u2_components_stay_inside_the_text_column(tabs, path, width, scheme):
    """U2: code, tabs, callouts, tables, images, diagrams and quotes fit the text column (1px tolerance)."""
    survey = tabs(width, scheme).survey(path)
    assert not survey.outside, "Elements stick out of the text column:\n" + "\n".join(
        f"  {o['element']} spans {o['left']}-{o['right']}px, the column is {o['columnLeft']}-{o['columnRight']}px"
        + (f" (judged by its scrolling parent {o['judgedBy']})" if o["judgedBy"] else "")
        for o in survey.outside
    )


@pytest.mark.parametrize("path, width, scheme", LAYOUT_CASES)
def test_u3_wide_content_scrolls_instead_of_being_cut_off(tabs, path, width, scheme):
    """U3: a line that is too wide scrolls inside its own block; nothing is clipped without a scrollbar."""
    survey = tabs(width, scheme).survey(path)
    assert not survey.code_blocks_that_do_not_scroll, f"Code blocks that cannot scroll: {survey.code_blocks_that_do_not_scroll}"
    assert not survey.clipped, "Content is cut off without a scrollbar:\n" + "\n".join(
        f"  {c['element']}: content is {c['scrollWidth']}px wide in a {c['clientWidth']}px box (overflow-x: {c['overflowX']})"
        for c in survey.clipped
    )


@pytest.mark.parametrize("path, width, scheme", LAYOUT_CASES)
def test_u4_no_console_errors_or_failed_requests(tabs, path, width, scheme):
    """U4: no console errors, no uncaught errors, and no failed or >=400 requests to the site itself."""
    survey = tabs(width, scheme).survey(path)
    assert not survey.problems, "The page reported problems while loading:\n" + "\n".join(f"  {p}" for p in survey.problems)


@pytest.mark.parametrize(
    "scheme", [pytest.param(s, marks=pytest.mark.xdist_group(f"layout-320-{s}")) for s in SCHEMES], ids=SCHEMES
)
def test_u3_a_long_code_line_really_scrolls_in_its_own_block(tabs, scheme):
    """U3 (positive check): in the Conventions page, scrolling the deliberately long line moves only that block."""
    tab = tabs(320, scheme)
    tab.visit("conventions/")
    result = tab.page.evaluate(
        """() => {
          const code = [...document.querySelectorAll('pre > code')].find(c => c.textContent.includes('deliberately much wider'));
          if (!code) return { found: false };
          const before = code.scrollLeft;
          code.scrollLeft = 10000;
          return { found: true, canScroll: code.scrollWidth > code.clientWidth, moved: code.scrollLeft > before,
                   pageStillFits: document.documentElement.scrollWidth <= document.documentElement.clientWidth };
        }"""
    )
    assert result["found"], "The long-line example is missing from the Conventions page."
    assert result["canScroll"] and result["moved"], "The long line did not scroll inside its block."
    assert result["pageStillFits"], "Scrolling the long line made the whole page scroll sideways."
