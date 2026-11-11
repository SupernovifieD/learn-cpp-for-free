"""Save full-page screenshots of every page for visual review (not a test).

    python tests/ui/screenshots.py

Writes artifacts/screenshots/<page>/<width>-<scheme>.png (git-ignored):
375 and 1280 px wide for every page, plus 320 px for pages that contain tabs,
tables or diagrams, in both color schemes. Uses the same browser setup as the
tests, so BASE_URL and MERMAID_JS work here too. Review the images against the
visual checklist V1-V12 in CONTRIBUTING.md.
"""

from pathlib import Path

from conftest import PAGES, REPO_ROOT, SCHEMES, Tab, new_context, page_id, start_server
from playwright.sync_api import sync_playwright

OUTPUT = REPO_ROOT / "artifacts" / "screenshots"
BASE_WIDTHS = [375, 1280]
EXTRA_NARROW_WIDTH = 320
NEEDS_NARROW_VIEW = "!!document.querySelector('.tabbed-set, table, .mermaid')"


def main() -> None:
    base_url, server = start_server()
    count = 0
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            for scheme in SCHEMES:
                for width in [EXTRA_NARROW_WIDTH, *BASE_WIDTHS]:
                    context = new_context(browser, width, scheme)
                    tab = Tab(context.new_page(), base_url)
                    for path in PAGES:
                        tab.visit(path)
                        if width == EXTRA_NARROW_WIDTH and not tab.page.evaluate(NEEDS_NARROW_VIEW):
                            continue
                        target = OUTPUT / page_id(path) / f"{width}-{scheme}.png"
                        target.parent.mkdir(parents=True, exist_ok=True)
                        tab.page.screenshot(path=str(target), full_page=True)
                        count += 1
                    context.close()
            browser.close()
    finally:
        if server:
            server.shutdown()
    print(f"Saved {count} screenshots to {Path(OUTPUT).relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main()
