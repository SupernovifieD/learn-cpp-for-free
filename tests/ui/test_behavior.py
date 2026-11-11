"""Behavior checks: how the site reacts to the reader."""

import pytest
import yaml
from conftest import PAGES, REPO_ROOT, Tab, new_context, page_id


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
