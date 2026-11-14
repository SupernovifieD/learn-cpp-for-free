"""Behavior checks: how the book reacts to the reader."""

import posixpath
import re

import pytest
from conftest import (
    BOOK_DIR,
    CONFIG,
    CONTENT,
    DIAGRAM_PAGES,
    PAGES,
    REPO_ROOT,
    SCHEMES,
    SIDEBAR_SHOWN_FROM,
    THEME_OF_SCHEME,
    Tab,
    built_pages,
    new_context,
    page_id,
    read_summary,
)

SUMMARY = read_summary()
CONVENTIONS = "conventions.html"
LESSON_0_5 = "ch00-getting-started/05-compiler-linker-and-libraries.html"
LESSON_0_6 = "ch00-getting-started/06-installing-an-ide.html"
LESSON_0_7 = "ch00-getting-started/07-compiling-your-first-program.html"


@pytest.fixture
def private_tab(browser, base_url):
    """A tab with its own storage, for tests that change what the book remembers about the reader."""
    contexts = []

    def make(width: int, scheme: str = "light", **options) -> Tab:
        context = new_context(browser, width, scheme, **options)
        contexts.append(context)
        return Tab(context.new_page(), base_url, width)

    yield make
    for context in contexts:
        context.close()


# ------------------------------------------------------------- navigation --


def test_every_built_page_is_in_the_summary():
    """Every chapter page that was built is listed in SUMMARY.md, and every listed page was built."""
    listed, built = set(PAGES), built_pages()
    assert listed == built, f"Listed but not built: {sorted(listed - built)}. Built but not listed: {sorted(built - listed)}."


@pytest.mark.parametrize("position", range(len(SUMMARY)), ids=[page_id(path) for _, path in SUMMARY])
def test_u8_previous_and_next_links_follow_the_summary_order(tabs, base_url, position):
    """U8: the previous and next arrows of a page lead to its neighbors in SUMMARY.md."""
    _, path = SUMMARY[position]
    tab = tabs(1280, "light")
    tab.visit(path)
    found = tab.page.evaluate(
        """() => { const read = (selector) => [...document.querySelectorAll(selector)].map(a => a.href);
                  return { prev: read('a.nav-chapters.previous, a.mobile-nav-chapters.previous'),
                           next: read('a.nav-chapters.next, a.mobile-nav-chapters.next') }; }"""
    )
    for direction, neighbor in (("prev", position - 1), ("next", position + 1)):
        links = found[direction]
        if not 0 <= neighbor < len(SUMMARY):
            assert not links, f"'{path}' is at the {'start' if direction == 'prev' else 'end'} of the book but has a {direction} link: {links}"
            continue
        expected = base_url + SUMMARY[neighbor][1]
        # One arrow beside the page for wide screens and one below it for narrow ones.
        assert len(links) == 2, f"'{path}' has {len(links)} {direction} links; expected the wide and the narrow one."
        assert set(links) == {expected}, f"The {direction} links on '{path}' go to {links}, but SUMMARY.md puts {expected} next to it."


@pytest.mark.parametrize("width", [375, 1280])
def test_u8_the_arrow_shown_at_this_width_and_the_arrow_keys_turn_the_page(private_tab, base_url, width):
    """U8: exactly one next arrow is on screen, clicking it opens the next page, and the arrow keys work too."""
    tab = private_tab(width)
    tab.visit(SUMMARY[0][1])
    arrows = tab.page.locator("a.nav-chapters.next, a.mobile-nav-chapters.next").locator("visible=true")
    assert arrows.count() == 1, f"{arrows.count()} next arrows are on screen at {width}px; expected one."
    arrows.first.click()
    tab.page.wait_for_url(base_url + SUMMARY[1][1])
    tab.page.keyboard.press("ArrowRight")
    tab.page.wait_for_url(base_url + SUMMARY[2][1])
    tab.page.keyboard.press("ArrowLeft")
    tab.page.wait_for_url(base_url + SUMMARY[1][1])


def test_the_home_page_is_served_at_the_book_address(tabs, base_url):
    """The address of the book itself (without index.html) shows the home page."""
    tab = tabs(1280, "light")
    tab.visit("")
    assert tab.page.locator(f"{CONTENT} h1").inner_text() == CONFIG["book"]["title"]
    assert not tab.events, f"The home page reported problems: {tab.events}"


SIDEBAR_STATE_JS = """() => {
  const sidebar = document.getElementById('mdbook-sidebar');
  const box = sidebar.getBoundingClientRect();
  return { onScreen: box.right > 1 && box.left < innerWidth,
           links: [...sidebar.querySelectorAll('.chapter a')].map(a => a.getAttribute('href')).filter(h => h && !h.includes('#')),
           active: [...sidebar.querySelectorAll('.chapter a.active')].map(a => a.textContent.trim()) };
}"""


@pytest.mark.parametrize("width", [375, 768, 1280])
def test_u12_the_sidebar_lists_every_page_and_opens_and_closes(private_tab, base_url, width):
    """U12: the sidebar holds the whole table of contents, marks the current page, and its button shows and hides it."""
    tab = private_tab(width)
    label, path = SUMMARY[3]
    tab.visit(path)
    page = tab.page
    state = page.evaluate(SIDEBAR_STATE_JS)
    assert len(state["links"]) == len(SUMMARY), f"The sidebar lists {len(state['links'])} pages, but SUMMARY.md lists {len(SUMMARY)}."
    assert state["active"] == [label], f"The sidebar marks {state['active']} as the current page, expected ['{label}']."
    starts_open = width >= SIDEBAR_SHOWN_FROM
    assert state["onScreen"] == starts_open, f"At {width}px the sidebar should start {'open' if starts_open else 'closed'}."

    toggle = page.locator("#mdbook-sidebar-toggle")
    for expected in (not starts_open, starts_open):
        toggle.click()
        page.wait_for_function(
            "(open) => document.documentElement.classList.contains('sidebar-visible') === open && document.getAnimations().every(a => a.playState !== 'running')",
            arg=expected,
            timeout=5_000,
        )
        page.wait_for_timeout(400)  # the sidebar slides with a CSS transition
        assert page.evaluate(SIDEBAR_STATE_JS)["onScreen"] == expected, f"The sidebar did not {'open' if expected else 'close'} at {width}px."

    if not starts_open:
        toggle.click()
        page.locator("#mdbook-sidebar .chapter a", has_text=SUMMARY[5][0]).click()
        page.wait_for_url(base_url + SUMMARY[5][1])


# ----------------------------------------------------------------- themes --


@pytest.mark.parametrize("width", [375, 1280])
def test_u7_the_theme_menu_offers_auto_light_and_navy_and_remembers_the_choice(private_tab, width):
    """U7: the theme button lists Auto, Light and Navy; a choice changes the page and survives a reload."""
    tab = private_tab(width, "light")
    tab.visit("index.html")
    page = tab.page
    read = "[document.documentElement.className.split(' ').filter(c => ['light', 'rust', 'coal', 'navy', 'ayu'].includes(c)).join(' '), getComputedStyle(document.documentElement).backgroundColor]"

    theme, light_background = page.evaluate(read)
    assert theme == "light", f"A reader whose system is light should start in the light theme, not '{theme}'."

    page.locator("#mdbook-theme-toggle").click()
    choices = page.locator("#mdbook-theme-list button").locator("visible=true").all_inner_texts()
    assert choices == ["Auto", "Light", "Navy"], f"The theme menu offers {choices}."

    page.locator("#mdbook-theme-navy").click()
    theme, dark_background = page.evaluate(read)
    assert theme == "navy" and dark_background != light_background, f"Choosing Navy gave theme '{theme}' and background {dark_background}."

    tab.visit(CONVENTIONS)
    assert page.evaluate(read)[0] == "navy", "The chosen theme was forgotten on the next page."

    page.locator("#mdbook-theme-toggle").click()
    page.locator("#mdbook-theme-default_theme").click()
    assert page.evaluate(read) == ["light", light_background], "Choosing Auto did not return to the system's light scheme."


@pytest.mark.parametrize("scheme", SCHEMES)
def test_u7_the_theme_follows_the_system_color_scheme(tabs, scheme):
    """U7: without a choice, the book uses the light theme on a light system and Navy on a dark one."""
    tab = tabs(1280, scheme)
    tab.visit("index.html")
    classes = tab.page.evaluate("document.documentElement.className").split()
    assert THEME_OF_SCHEME[scheme] in classes, f"With a {scheme} system the page has the classes {classes}."


# ----------------------------------------------------------------- search --


LESSON_2_12 = "ch02-functions-and-files/12-header-guards.html"
SEARCHES = [("linker", LESSON_0_5), ("header guard", LESSON_2_12)]


@pytest.mark.parametrize("width", [375, 1280])
@pytest.mark.parametrize("query, lesson", SEARCHES, ids=[query.replace(" ", "-") for query, _ in SEARCHES])
def test_u9_searching_lists_the_lesson_that_explains_the_word(private_tab, base_url, width, query, lesson):
    """U9: typing 'linker' lists lesson 0.5 and 'header guard' lists lesson 2.12 among the results, and a result opens it."""
    tab = private_tab(width)
    tab.visit("index.html")
    page = tab.page
    page.locator("#mdbook-search-toggle").click()
    # Type like a reader does. An instant fill() can fire before the search index has loaded.
    page.locator("#mdbook-searchbar").press_sequentially(query, delay=60)
    page.wait_for_selector("#mdbook-searchresults li a", timeout=15_000)
    links = page.eval_on_selector_all("#mdbook-searchresults li a", "links => links.map(a => a.getAttribute('href'))")
    matching = [href for href in links if lesson in href]
    assert matching, f"Searching for '{query}' did not list {lesson}. The results were: {links}"
    page.locator(f'#mdbook-searchresults li a[href="{matching[0]}"]').first.click()
    page.wait_for_url(lambda url: url.startswith(base_url + lesson))
    assert not tab.events, f"Opening a search result reported problems: {tab.events}"


# --------------------------------------------------------------- diagrams --

DIAGRAM_JS = """(content) => {
  const inner = document.querySelector(content);
  const style = getComputedStyle(inner);
  const box = inner.getBoundingClientRect();
  const left = box.left + parseFloat(style.paddingLeft), right = box.right - parseFloat(style.paddingRight);
  const hosts = [...document.querySelectorAll('pre.mermaid')];
  return {
    hosts: hosts.length,
    drawn: hosts.filter(h => h.querySelector('svg')).length,
    pageFits: document.documentElement.scrollWidth <= document.documentElement.clientWidth,
    diagrams: hosts.map(h => {
      const svg = h.querySelector('svg');
      if (!svg) return null;
      const r = svg.getBoundingClientRect();
      const scale = r.width / svg.viewBox.baseVal.width;
      const fonts = [...svg.querySelectorAll('text, span, p, div')].map(e => parseFloat(getComputedStyle(e).fontSize)).filter(n => n > 0);
      const label = svg.querySelector('.nodeLabel');
      return { left: Math.round(r.left), right: Math.round(r.right), columnLeft: Math.round(left), columnRight: Math.round(right),
               smallestTextPx: fonts.length ? +(Math.min(...fonts) * scale).toFixed(1) : null,
               textColor: label ? getComputedStyle(label).color : null };
    }),
  };
}"""


def _brightness(color: str) -> float:
    red, green, blue = (float(part) for part in color[color.index("(") + 1 : color.index(")")].split(",")[:3])
    return 0.299 * red + 0.587 * green + 0.114 * blue


# Every page whose built HTML has a diagram is checked, so a diagram in a later lesson is tested the day it is added.
DIAGRAM_CASES = [pytest.param(path, 320, scheme, id=f"{page_id(path)}-320-{scheme}") for scheme in SCHEMES for path in DIAGRAM_PAGES]


def test_u10_the_pages_with_diagrams_are_found_in_the_built_book():
    """U10: the list of pages with a diagram comes from the built HTML; an empty list would test nothing."""
    assert LESSON_0_5 in DIAGRAM_PAGES and CONVENTIONS in DIAGRAM_PAGES, f"Lesson 0.5 and the Conventions page have diagrams, but the list is {DIAGRAM_PAGES}."


@pytest.mark.parametrize("path, width, scheme", DIAGRAM_CASES)
def test_u10_every_diagram_renders_and_fits_at_320(tabs, path, width, scheme):
    """U10: each diagram draws an <svg> in both color schemes, fits at 320px and keeps its text readable."""
    tab = tabs(width, scheme)
    tab.visit(path)  # also fails with a clear message if the diagram never renders
    found = tab.page.evaluate(DIAGRAM_JS, CONTENT)
    assert found["hosts"] >= 1, f"{path} has no diagram."
    assert found["drawn"] == found["hosts"], f"{found['hosts'] - found['drawn']} diagram(s) did not render an <svg>."
    assert found["pageFits"], "The diagram makes the page scroll sideways at 320px."
    for diagram in found["diagrams"]:
        assert diagram["left"] >= diagram["columnLeft"] - 1 and diagram["right"] <= diagram["columnRight"] + 1, (
            f"The diagram spans {diagram['left']}-{diagram['right']}px but the text column is {diagram['columnLeft']}-{diagram['columnRight']}px."
        )
        assert diagram["smallestTextPx"] is None or diagram["smallestTextPx"] >= 12, (
            f"The diagram is scaled down so far that its text is {diagram['smallestTextPx']}px; the minimum is 12px. "
            "Use fewer nodes per row or shorter labels."
        )
        assert diagram["textColor"] is not None, "The diagram has no node labels, so its colors cannot be checked. Write it as `flowchart TD`."
        # Mermaid's dark theme has light text and its default theme dark text.
        bright = _brightness(diagram["textColor"]) > 128
        assert bright == (scheme == "dark"), f"In the {scheme} scheme the diagram's text is {diagram['textColor']}: it was drawn for the other scheme."


def test_u10_a_diagram_is_redrawn_when_the_theme_changes(private_tab):
    """U10: switching from the light theme to Navy redraws the diagram with Mermaid's dark colors."""
    tab = private_tab(1280, "light")
    tab.visit(LESSON_0_5)
    page = tab.page
    before = page.evaluate(DIAGRAM_JS, CONTENT)["diagrams"][0]["textColor"]
    page.locator("#mdbook-theme-toggle").click()
    with page.expect_navigation():  # the page reloads itself to draw the diagram again
        page.locator("#mdbook-theme-navy").click()
    page.wait_for_function("[...document.querySelectorAll('pre.mermaid')].every(d => d.querySelector('svg'))", timeout=20_000)
    after = page.evaluate(DIAGRAM_JS, CONTENT)["diagrams"][0]["textColor"]
    assert _brightness(before) < 128 < _brightness(after), f"The diagram's text went from {before} to {after}."


# ------------------------------------------------------------------- tabs --

TABS_JS = """() => [...document.querySelectorAll('.tabs')].map(group => {
  const tabs = [...group.querySelectorAll('[role=tab]')];
  const panels = [...group.querySelectorAll(':scope > .tab')];
  const shown = (el) => el.getBoundingClientRect().height > 0;
  return {
    hasTablist: !!group.querySelector('[role=tablist][aria-label]'),
    labels: tabs.map(t => t.textContent),
    selected: tabs.filter(t => t.getAttribute('aria-selected') === 'true').map(t => t.textContent),
    tabStops: tabs.filter(t => t.tabIndex === 0).length,
    shownPanels: panels.filter(shown).map(p => p.dataset.tab),
    wired: tabs.every((t, i) => t.getAttribute('aria-controls') === panels[i].id && panels[i].getAttribute('aria-labelledby') === t.id
                                 && panels[i].getAttribute('role') === 'tabpanel'),
    staticLabelsShown: [...group.querySelectorAll('.tab-label')].filter(shown).length,
    tallEnough: tabs.every(t => t.getBoundingClientRect().height >= 44),
  };
})"""

OS_LABELS = ["Windows", "macOS", "Linux"]
TOOL_LABELS = ["Visual Studio", "VS Code", "Command line"]


@pytest.mark.parametrize("width", [320, 1280])
def test_u13_tabs_are_accessible_and_show_one_panel(private_tab, width):
    """U13: each group is a tablist with one selected tab, one visible panel and usable touch targets."""
    tab = private_tab(width)
    tab.visit(CONVENTIONS)
    groups = tab.page.evaluate(TABS_JS)
    assert [group["labels"] for group in groups] == [OS_LABELS, TOOL_LABELS], f"The Conventions page has these tabs: {groups}"
    for group in groups:
        first = group["labels"][0]
        assert group["hasTablist"] and group["wired"], f"The tabs {group['labels']} lack tablist, tab or tabpanel wiring."
        assert group["selected"] == [first] and group["shownPanels"] == [first], f"Expected only '{first}' to be selected and shown: {group}"
        assert group["tabStops"] == 1, "Exactly one tab of a group may be a Tab-key stop; the arrow keys reach the others."
        assert group["staticLabelsShown"] == 0, "The labels meant for readers without JavaScript are showing next to the tabs."
        assert group["tallEnough"], "A tab is less than 44px tall, which is too small for a finger."


def test_u13_tabs_work_with_the_keyboard_without_turning_the_page(private_tab, base_url):
    """U13: the arrow, Home and End keys move between tabs, and do not trigger mdBook's page-turning keys."""
    tab = private_tab(1280)
    tab.visit(CONVENTIONS)
    page = tab.page
    page.locator("[role=tab]", has_text="Windows").focus()
    for key, expected in [("ArrowRight", "macOS"), ("ArrowRight", "Linux"), ("ArrowRight", "Windows"), ("ArrowLeft", "Linux"), ("Home", "Windows"), ("End", "Linux")]:
        page.keyboard.press(key)
        group = page.evaluate(TABS_JS)[0]
        focused = page.evaluate("document.activeElement.textContent")
        assert group["selected"] == [expected] and group["shownPanels"] == [expected] and focused == expected, (
            f"After {key}, expected '{expected}' to be selected, shown and focused; got {group['selected']}, {group['shownPanels']}, '{focused}'."
        )
    assert page.url == base_url + CONVENTIONS, f"An arrow key inside the tabs turned the page to {page.url}."


def test_u13_a_chosen_tab_is_remembered_across_groups_and_pages(private_tab):
    """U13: choosing macOS selects it in every operating-system group in the book, and leaves other groups alone."""
    tab = private_tab(375)
    tab.visit(CONVENTIONS)
    page = tab.page
    page.locator("[role=tab]", has_text="macOS").click()
    page.locator("[role=tab]", has_text="Command line").click()
    groups = page.evaluate(TABS_JS)
    assert [group["shownPanels"] for group in groups] == [["macOS"], ["Command line"]], f"After two clicks the page shows {groups}"

    tab.visit(LESSON_0_6)
    assert [group["selected"] for group in page.evaluate(TABS_JS)] == [["macOS"]], "Lesson 0.6 did not open on the macOS tab."
    tab.visit(LESSON_0_7)
    assert [group["selected"] for group in page.evaluate(TABS_JS)] == [["Command line"]], "Lesson 0.7 did not open on the Command line tab."


def test_u13_without_javascript_every_tab_is_readable(private_tab):
    """U13: with JavaScript off, all the instructions are shown one after another, each under its label."""
    tab = private_tab(375, java_script_enabled=False)
    tab.page.goto(tab.base_url + LESSON_0_6, wait_until="load")
    found = tab.page.evaluate(
        """() => { const shown = (el) => el.getBoundingClientRect().height > 0;
                  return { labels: [...document.querySelectorAll('.tab-label')].filter(shown).map(l => l.textContent),
                           panels: [...document.querySelectorAll('.tab')].filter(shown).length,
                           buttons: document.querySelectorAll('[role=tab]').length,
                           pageFits: document.documentElement.scrollWidth <= document.documentElement.clientWidth }; }"""
    )
    assert found["labels"] == OS_LABELS and found["panels"] == 3, f"Without JavaScript the page shows {found}."
    assert found["buttons"] == 0 and found["pageFits"]


# ------------------------------------------------- questions and answers --


@pytest.mark.parametrize("width", [375, 1280])
def test_u14_answers_stay_hidden_until_the_reader_opens_them(private_tab, width):
    """U14: a question is collapsed, opening it shows the question but not the answer, and the keyboard works."""
    tab = private_tab(width)
    tab.visit(CONVENTIONS)
    page = tab.page
    # Other questions may be added to this page, so the one tested here is found by its summary and its text.
    question = page.locator(f"{CONTENT} > details").filter(
        has=page.locator("> summary", has_text=re.compile(r"^Check your understanding$")),
        has_text="Which callout type marks a habit",
    )
    answer = question.locator("details")
    assert question.count() == 1 and answer.count() == 1, "The Conventions page should have one question about callouts, with one answer."
    assert question.locator("> summary").inner_text() == "Check your understanding"
    assert not question.evaluate("d => d.open"), "The question is open when the page loads."
    assert not page.get_by_text("The best practice callout.").is_visible(), "The answer can be seen before the reader asks for it."

    question.locator("> summary").click()
    assert page.get_by_text("Which callout type marks a habit").is_visible(), "Opening the question did not show it."
    assert not answer.evaluate("d => d.open") and not page.get_by_text("The best practice callout.").is_visible(), "Opening the question also revealed the answer."

    answer.locator("> summary").focus()
    page.keyboard.press("Enter")
    assert page.get_by_text("The best practice callout.").is_visible(), "Pressing Enter on 'Answer' did not show the answer."
    page.keyboard.press("Enter")
    assert not page.get_by_text("The best practice callout.").is_visible(), "Pressing Enter again did not hide the answer."


# ------------------------------------------------------------- code blocks --


def test_u15_the_copy_button_copies_the_program_and_no_block_can_be_run(private_tab):
    """U15: every code block has a copy button that copies its exact text, and none has a Rust run button."""
    tab = private_tab(1280, permissions=["clipboard-read", "clipboard-write"])
    tab.visit(LESSON_0_7)
    page = tab.page
    blocks = page.locator(f"{CONTENT} pre:not(.mermaid)")
    assert blocks.count() > 0 and page.locator(f"{CONTENT} pre:not(.mermaid) .clip-button").count() == blocks.count(), "A code block has no copy button."
    assert page.locator(".play-button").count() == 0, "A code block has a run button."

    program = blocks.first
    program.hover()
    program.locator(".clip-button").click()
    copied = page.evaluate("navigator.clipboard.readText()")
    source = (REPO_ROOT / "examples" / "ch00" / "07-hello-world.cpp").read_text()
    assert copied.rstrip("\n") == source.rstrip("\n"), f"The copy button copied {copied!r}, not the program in examples/."


def test_u15_code_blocks_are_labeled_and_highlighted(tabs):
    """U15: a program shows its file name, output is labeled, and C++ and PowerShell are both highlighted."""
    tab = tabs(1280, "light")
    tab.visit(LESSON_0_7)
    found = tab.page.evaluate(
        """() => ({ labels: [...document.querySelectorAll('figure.listing > .file-name')].map(l => l.textContent),
                   cpp: document.querySelectorAll('code.language-cpp [class^=hljs-]').length,
                   powershell: document.querySelectorAll('code.language-powershell [class^=hljs-]').length,
                   literal: document.querySelector('main').textContent.includes('{{#') })"""
    )
    assert found["labels"] == ["Filename: hello-world.cpp", "Output"], f"The code labels on lesson 0.7 are {found['labels']}."
    assert found["cpp"] > 0, "The C++ program is not syntax-highlighted."
    assert found["powershell"] > 0, "The PowerShell commands are not syntax-highlighted."
    assert not found["literal"], "An include or tab marker is printed as text on the page."


# ---------------------------------------------------------- links and URLs --


@pytest.mark.parametrize("path", PAGES, ids=[page_id(p) for p in PAGES])
def test_u16_edit_and_repository_links_point_at_the_page_source(tabs, path):
    """U16: 'Suggest an edit' opens this page's Markdown file on GitHub, and the repository link the repository."""
    tab = tabs(1280, "light")
    tab.visit(path)
    repository = CONFIG["output"]["html"]["git-repository-url"]
    source = "docs/" + posixpath.splitext(path)[0] + ".md"
    assert (REPO_ROOT / source).is_file(), f"{source} does not exist."
    assert tab.page.locator("a[rel=edit]").get_attribute("href") == f"{repository}/edit/main/{source}"
    assert tab.page.locator(".right-buttons a[title='Git repository']").get_attribute("href") == repository


@pytest.mark.parametrize("path", PAGES, ids=[page_id(p) for p in PAGES])
def test_u16_links_between_pages_lead_to_pages_and_headings_that_exist(tabs, base_url, path):
    """U16: every link in a page's content that stays inside the book leads to a built page, and its #fragment to an element."""
    tab = tabs(1280, "light")
    tab.visit(path)
    links = tab.page.eval_on_selector_all(f"{CONTENT} a[href]", "links => links.map(a => a.href)")
    for link in links:
        if not link.startswith(base_url):
            continue
        target, _, fragment = link[len(base_url) :].partition("#")
        file = BOOK_DIR / (target or "index.html")
        assert file.is_file(), f"'{path}' links to {link}, which was not built."
        if fragment:
            assert f'id="{fragment}"' in file.read_text(), f"'{path}' links to {link}, but that page has no element with the id '{fragment}'."


def test_u17_an_unknown_address_shows_a_styled_404_page(private_tab, base_url):
    """U17: the 'not found' page loads its styles and scripts from the book's address, even from a deeper path.

    This is also what a reader sees at an address from before the move to mdBook, such as /conventions/.
    """
    tab = private_tab(1280)
    page = tab.page
    tab.events.clear()
    page.goto(base_url + "no-such-chapter/no-such-page.html", wait_until="load")
    page.wait_for_selector("#mdbook-sidebar .chapter a", state="attached", timeout=10_000)
    assert "not found" in page.locator(f"{CONTENT}").inner_text().lower()
    # The address itself answers 404, which the browser also logs once as a console error without a URL.
    failed = [event for event in tab.events if not event.startswith("console error: Failed to load resource")]
    assert len(failed) == 1 and "no-such-page.html" in failed[0], f"The 404 page failed to load some of its files: {failed}"
    assert len(tab.events) == 2, f"The 404 page reported more than its own address: {tab.events}"
    page.locator("#mdbook-sidebar .chapter a").first.click()
    page.wait_for_url(base_url + SUMMARY[0][1])
