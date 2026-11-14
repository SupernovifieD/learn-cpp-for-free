"""Layout checks U1-U4 (and U18, the same checks with every answer opened): every page, at every viewport width, in both color schemes.

Each (page, width, scheme) is loaded once and measured once (see Tab.survey in
conftest.py); the tests below only read that measurement.
"""

import pytest
from conftest import DETAILS_PAGES, PAGES, SCHEMES, WIDTHS, page_id

# Run in parallel, all the tests of one width and color scheme go to the same worker (see
# pytest_xdist_make_scheduler in conftest.py), so each page is loaded once and all checks reuse it.
LAYOUT_CASES = [
    pytest.param(path, width, scheme, id=f"{page_id(path)}-{width}-{scheme}")
    for scheme in SCHEMES
    for width in WIDTHS
    for path in PAGES
]

# The same measurements for the pages that have questions, with every <details> opened. Answers are
# closed when a page loads, so the checks above never see the code and diagrams inside them.
OPENED_WIDTHS = [320, 375, 1280]
OPENED_CASES = [
    pytest.param(path, width, scheme, id=f"{page_id(path)}-open-{width}-{scheme}")
    for scheme in SCHEMES
    for width in OPENED_WIDTHS
    for path in DETAILS_PAGES
]


def check_no_page_scroll(survey):
    assert survey.scroll_width <= survey.client_width, (
        f"The page scrolls sideways: it is {survey.scroll_width}px wide in a {survey.client_width}px window."
    )
    # mdBook's text area scrolls on its own, so an element that is too wide leaves the document alone and shows
    # up only here.
    assert survey.area_scroll_width <= survey.area_client_width + 1, (
        f"The text area scrolls sideways: its content is {survey.area_scroll_width}px wide in a {survey.area_client_width}px area, "
        "so something is wider than the text column."
    )


def check_inside_text_column(survey):
    assert not survey.outside, "Elements stick out of the text column:\n" + "\n".join(
        f"  {o['element']} spans {o['left']}-{o['right']}px, the column is {o['columnLeft']}-{o['columnRight']}px"
        + (f" (judged by its scrolling parent {o['judgedBy']})" if o["judgedBy"] else "")
        for o in survey.outside
    )


def check_wide_content_scrolls(survey):
    assert not survey.code_blocks_that_do_not_scroll, f"Code blocks that cannot scroll: {survey.code_blocks_that_do_not_scroll}"
    assert not survey.clipped, "Content is cut off without a scrollbar:\n" + "\n".join(
        f"  {c['element']}: content is {c['scrollWidth']}px wide in a {c['clientWidth']}px box (overflow-x: {c['overflowX']})"
        for c in survey.clipped
    )


def check_no_console_errors(survey):
    assert not survey.problems, "The page reported problems while loading:\n" + "\n".join(f"  {p}" for p in survey.problems)


@pytest.mark.parametrize("path, width, scheme", LAYOUT_CASES)
def test_u1_no_horizontal_page_scroll(tabs, path, width, scheme):
    """U1: the page, and the text area inside it, is never wider than the window."""
    check_no_page_scroll(tabs(width, scheme).survey(path))


@pytest.mark.parametrize("path, width, scheme", LAYOUT_CASES)
def test_u2_components_stay_inside_the_text_column(tabs, path, width, scheme):
    """U2: code, tabs, callouts, tables, images, diagrams and quotes fit the text column (1px tolerance)."""
    check_inside_text_column(tabs(width, scheme).survey(path))


@pytest.mark.parametrize("path, width, scheme", LAYOUT_CASES)
def test_u3_wide_content_scrolls_instead_of_being_cut_off(tabs, path, width, scheme):
    """U3: a line that is too wide scrolls inside its own block; nothing is clipped without a scrollbar."""
    check_wide_content_scrolls(tabs(width, scheme).survey(path))


@pytest.mark.parametrize("path, width, scheme", LAYOUT_CASES)
def test_u4_no_console_errors_or_failed_requests(tabs, path, width, scheme):
    """U4: no console errors, no uncaught errors, and no failed or >=400 requests to the site itself."""
    check_no_console_errors(tabs(width, scheme).survey(path))


# -------------------------------------------------- U18: every answer opened --


@pytest.mark.parametrize("path, width, scheme", OPENED_CASES)
def test_u18_opened_answers_never_make_the_page_scroll_sideways(tabs, path, width, scheme):
    """U18 (U1 with every answer opened): the page is never wider than the window."""
    check_no_page_scroll(tabs(width, scheme).survey(path, open_details=True))


@pytest.mark.parametrize("path, width, scheme", OPENED_CASES)
def test_u18_opened_answers_stay_inside_the_text_column(tabs, path, width, scheme):
    """U18 (U2 with every answer opened): code, callouts, tables and diagrams inside answers fit the text column."""
    check_inside_text_column(tabs(width, scheme).survey(path, open_details=True))


@pytest.mark.parametrize("path, width, scheme", OPENED_CASES)
def test_u18_wide_content_in_opened_answers_scrolls_instead_of_being_cut_off(tabs, path, width, scheme):
    """U18 (U3 with every answer opened): long lines inside answers scroll in their own block."""
    check_wide_content_scrolls(tabs(width, scheme).survey(path, open_details=True))


@pytest.mark.parametrize("path, width, scheme", OPENED_CASES)
def test_u18_opening_the_answers_causes_no_errors_and_leaves_no_diagram_without_size(tabs, path, width, scheme):
    """U18 (U4 with every answer opened): no console errors, and a diagram inside an answer has a size once opened."""
    survey = tabs(width, scheme).survey(path, open_details=True)
    check_no_console_errors(survey)
    assert not survey.empty_diagrams, f"Diagrams with no size after opening the answers: {survey.empty_diagrams}"


def test_u18_the_pages_with_answers_are_found_in_the_built_book():
    """U18: the list of pages with a <details> comes from the built HTML; an empty list would test nothing."""
    assert "conventions.html" in DETAILS_PAGES, f"The Conventions page has questions but is not in {DETAILS_PAGES}."
    assert len(OPENED_CASES) == len(DETAILS_PAGES) * len(OPENED_WIDTHS) * len(SCHEMES)


@pytest.mark.parametrize(
    "scheme", [pytest.param(s) for s in SCHEMES], ids=SCHEMES
)
def test_u3_a_long_code_line_really_scrolls_in_its_own_block(tabs, scheme):
    """U3 (positive check): in the Conventions page, scrolling the deliberately long line moves only that block."""
    tab = tabs(320, scheme)
    tab.visit("conventions.html")
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
