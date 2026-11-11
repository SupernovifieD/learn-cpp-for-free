"""Behavior checks: how the site reacts to the reader."""

import pytest
from conftest import Tab, new_context


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
