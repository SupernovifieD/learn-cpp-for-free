"""Save full-page screenshots of the pages for visual review (not a test).

    python tests/ui/screenshots.py
    python tests/ui/screenshots.py --open-details --only ch01
    python tests/ui/screenshots.py --widths 320,375,768,1280,1920

Writes artifacts/screenshots/<page>/<width>-<scheme>.png (git-ignored): 375 and 1280 px wide for
every page, plus 320 px for pages that contain tabs, tables or diagrams, in both color schemes. Uses
the same browser setup as the tests, so BASE_URL works here too. Review the images against the visual
checklist in CONTRIBUTING.md.

Options:
  --open-details  Open every <details> (every question and answer) before the picture, save it as
                  <width>-<scheme>-open.png, and only visit the pages that have one.
  --only TEXT     Only the pages whose path contains TEXT (for example ch01 or 05-).
  --widths LIST   Comma-separated widths for every selected page, instead of the default rule above.
"""

import argparse
from pathlib import Path

from conftest import DETAILS_PAGES, PAGES, REPO_ROOT, SCHEMES, Tab, new_context, page_id, start_server
from playwright.sync_api import sync_playwright

OUTPUT = REPO_ROOT / "artifacts" / "screenshots"
BASE_WIDTHS = [375, 1280]
EXTRA_NARROW_WIDTH = 320
NEEDS_NARROW_VIEW = "!!document.querySelector('.tabs, table, .mermaid')"


def main() -> None:
    parser = argparse.ArgumentParser(description="Save screenshots of the book's pages for visual review.")
    parser.add_argument("--open-details", action="store_true", help="open every <details> and save <width>-<scheme>-open.png")
    parser.add_argument("--only", default="", help="only pages whose path contains this text")
    parser.add_argument("--widths", default="", help="comma-separated widths for every selected page (default: 375 and 1280, plus 320 where needed)")
    args = parser.parse_args()

    widths = [int(width) for width in args.widths.split(",") if width.strip()]
    pages = [path for path in (DETAILS_PAGES if args.open_details else PAGES) if args.only in path]
    if not pages:
        raise SystemExit(f"No page matches --only {args.only!r}" + (" and has a <details>." if args.open_details else "."))
    suffix = "-open" if args.open_details else ""

    base_url, server = start_server()
    count = 0
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            for scheme in SCHEMES:
                for width in widths or [EXTRA_NARROW_WIDTH, *BASE_WIDTHS]:
                    context = new_context(browser, width, scheme)
                    tab = Tab(context.new_page(), base_url)
                    for path in pages:
                        tab.visit(path, open_details=args.open_details)
                        if not widths and width == EXTRA_NARROW_WIDTH and not tab.page.evaluate(NEEDS_NARROW_VIEW):
                            continue
                        target = OUTPUT / page_id(path) / f"{width}-{scheme}{suffix}.png"
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
