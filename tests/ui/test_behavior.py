"""Behavior checks: how the site reacts to the reader."""

import pytest
import yaml
from conftest import PAGES, REPO_ROOT, SCHEMES, Tab, new_context, page_id


class _TolerantLoader(yaml.SafeLoader):
    """Reads mkdocs.yml although it contains Python-specific tags such as !!python/name:..."""


_TolerantLoader.add_multi_constructor("tag:yaml.org,2002:python/name:", lambda loader, suffix, node: None)


def read_nav() -> list[tuple[str | None, str]]:
    """The pages listed in mkdocs.yml's nav, in order, as (label, url_path).

    The label is None for a page listed without one. A chapter's index page is listed
    without a label, so it takes the chapter's label.
    """
    config = yaml.load((REPO_ROOT / "mkdocs.yml").read_text(), Loader=_TolerantLoader)
    pages: list[tuple[str | None, str]] = []

    def to_url_path(markdown_path: str) -> str:
        stem = markdown_path.removesuffix(".md")
        if stem == "index":
            return ""
        return stem.removesuffix("/index") + "/" if stem.endswith("/index") else stem + "/"

    def walk(items, chapter_label=None):
        for item in items:
            if isinstance(item, str):
                pages.append((chapter_label, to_url_path(item)))
                continue
            for label, value in item.items():
                if isinstance(value, str):
                    pages.append((label, to_url_path(value)))
                else:
                    walk(value, label)

    walk(config["nav"])
    return pages


NAV = read_nav()


def test_every_built_page_is_in_the_nav():
    """Every page that was built is reachable from the nav, and the nav lists no page that was not built."""
    in_nav = {path for _, path in NAV}
    assert in_nav == set(PAGES), (
        f"In the nav but not built: {sorted(in_nav - set(PAGES))}. Built but not in the nav: {sorted(set(PAGES) - in_nav)}."
    )


@pytest.mark.xdist_group("nav-order")
@pytest.mark.parametrize("position", range(len(NAV)), ids=[page_id(path) for _, path in NAV])
def test_u8_footer_links_follow_the_nav_order(tabs, base_url, position):
    """U8: the Previous and Next links at the bottom of a page lead to its neighbors in the nav."""
    label, path = NAV[position]
    tab = tabs(1280, "light")
    tab.visit(path)
    found = tab.page.evaluate(
        """() => { const read = (a) => a ? { href: a.href, label: a.getAttribute('aria-label') } : null;
                  return { prev: read(document.querySelector('.md-footer__link--prev')),
                           next: read(document.querySelector('.md-footer__link--next')) }; }"""
    )
    for direction, neighbor in (("prev", position - 1), ("next", position + 1)):
        link = found[direction]
        if not 0 <= neighbor < len(NAV):
            assert link is None, f"'{path or 'index'}' is at the {'start' if direction == 'prev' else 'end'} of the nav but has a {direction} link: {link}"
            continue
        neighbor_label, neighbor_path = NAV[neighbor]
        assert link is not None, f"'{path or 'index'}' has no {direction} link; expected one to '{neighbor_path or 'index'}'."
        assert link["href"] == base_url + neighbor_path, (
            f"The {direction} link on '{path or 'index'}' goes to {link['href']}, but the nav puts '{neighbor_path or 'index'}' next to it."
        )
        if neighbor_label:
            word = "Previous" if direction == "prev" else "Next"
            assert link["label"] == f"{word}: {neighbor_label}", f"The {direction} link is labeled '{link['label']}', expected '{word}: {neighbor_label}'."


@pytest.mark.parametrize("width", [375, 1280])
def test_u7_palette_toggle_cycles_color_schemes(browser, base_url, width):
    """U7: the header button cycles system -> light -> dark -> system, and the page changes color scheme."""
    # A private context: Material stores the reader's choice in localStorage, which would leak into other tests.
    context = new_context(browser, width, "light")
    try:
        tab = Tab(context.new_page(), base_url)
        tab.visit("")
        read = "[document.body.dataset.mdColorMedia, document.body.dataset.mdColorScheme]"
        seen = [tab.page.evaluate(read)]
        for _ in range(3):
            tab.page.locator('[data-md-component="palette"] label:visible').click()
            seen.append(tab.page.evaluate(read))
        medias = [media for media, _ in seen]
        schemes = [scheme for _, scheme in seen]
        assert medias == [
            "(prefers-color-scheme)",
            "(prefers-color-scheme: light)",
            "(prefers-color-scheme: dark)",
            "(prefers-color-scheme)",
        ], f"The toggle did not step through system, light and dark in order: {medias}"
        assert schemes == ["default", "default", "slate", "default"], (
            f"The color scheme did not change as expected (system is light here): {schemes}"
        )
    finally:
        context.close()


LESSON_0_5 = "ch00-getting-started/05-compiler-linker-and-libraries/"
SEARCH_FIELD_SHOWN_FROM = 960  # px; below this Material hides the field behind the search icon


@pytest.mark.xdist_group("search")
@pytest.mark.parametrize("width", [375, 1280])
def test_u9_searching_for_linker_lists_lesson_0_5(browser, base_url, width):
    """U9: typing 'linker' into the search box lists lesson 0.5 among the results."""
    context = new_context(browser, width, "light")
    try:
        tab = Tab(context.new_page(), base_url)
        tab.visit("")
        page = tab.page
        if width < SEARCH_FIELD_SHOWN_FROM:
            page.locator('label.md-header__button[for="__search"]').click()
        # Type like a reader does. An instant fill() can fire before Material has loaded its search index.
        page.locator(".md-search__input").press_sequentially("linker", delay=60)
        page.wait_for_selector(".md-search-result__item", timeout=15_000)
        links = page.eval_on_selector_all(".md-search-result__link", "links => links.map(a => a.getAttribute('href'))")
        assert any(LESSON_0_5 in href for href in links), (
            f"Searching for 'linker' did not list lesson 0.5. The results were: {links}"
        )
    finally:
        context.close()


DIAGRAM_JS = """() => {
  const inner = document.querySelector('.md-content__inner');
  const style = getComputedStyle(inner);
  const box = inner.getBoundingClientRect();
  const left = box.left + parseFloat(style.paddingLeft), right = box.right - parseFloat(style.paddingRight);
  const hosts = [...document.querySelectorAll('.mermaid')];
  return {
    hosts: hosts.length,
    drawn: hosts.filter(h => h.shadowRoot && h.shadowRoot.querySelector('svg')).length,
    pageFits: document.documentElement.scrollWidth <= document.documentElement.clientWidth,
    diagrams: hosts.map(h => {
      const svg = h.shadowRoot && h.shadowRoot.querySelector('svg');
      if (!svg) return null;
      const r = svg.getBoundingClientRect();
      const scale = r.width / svg.viewBox.baseVal.width;
      const fonts = [...svg.querySelectorAll('text, span, p, div')].map(e => parseFloat(getComputedStyle(e).fontSize)).filter(n => n > 0);
      return { left: Math.round(r.left), right: Math.round(r.right), columnLeft: Math.round(left), columnRight: Math.round(right),
               smallestTextPx: fonts.length ? +(Math.min(...fonts) * scale).toFixed(1) : null };
    }),
  };
}"""


@pytest.mark.xdist_group("layout-320-light")
@pytest.mark.parametrize("scheme", SCHEMES)
def test_u10_lesson_0_5_diagram_renders_and_fits_at_320(tabs, scheme):
    """U10: the Mermaid diagram draws an <svg> in both color schemes, fits at 320px and keeps its text readable."""
    tab = tabs(320, scheme)
    tab.visit(LESSON_0_5)  # also fails with a clear message if the diagram never renders
    found = tab.page.evaluate(DIAGRAM_JS)
    assert found["hosts"] >= 1, "Lesson 0.5 has no diagram."
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
