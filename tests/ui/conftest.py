"""Shared helpers and fixtures for the browser tests (layout, accessibility, behavior).

The tests drive headless Chromium against the built book in book/ (run
`make build` first, or use `make test-ui`, which builds for you). The book is
served under the same path as on GitHub Pages (see `site-url` in book.toml), so
a link or an asset that only works at the root of a domain fails here.

Environment variable (optional):
  BASE_URL    Test an already published book, e.g. the live GitHub Pages URL,
              instead of serving the local book/ directory. The list of pages
              still comes from the local docs/SUMMARY.md.

This module also holds the small browser helpers that tests/ui/screenshots.py
reuses, so both always open pages the same way.
"""

from __future__ import annotations

import http.server
import os
import posixpath
import re
import threading
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
BOOK_DIR = REPO_ROOT / "book"
CONFIG = tomllib.loads((REPO_ROOT / "book.toml").read_text())
SITE_PATH = "/" + CONFIG["output"]["html"]["site-url"].strip("/") + "/"  # "/learn-cpp-for-free/"
FAILURE_SHOTS = REPO_ROOT / "artifacts" / "screenshots" / "failures"

# Viewport widths from the UI quality bar (height is always 800).
WIDTHS = [320, 360, 375, 414, 768, 1024, 1280, 1440, 1920]
SCHEMES = ["light", "dark"]

# The mdBook theme that each color scheme selects (see default-theme and preferred-dark-theme in book.toml).
THEME_OF_SCHEME = {"light": "light", "dark": "navy"}

# Widths at which axe-core also checks every page (U5). It runs on the same page load that the
# layout checks use, so the page is not loaded a second time.
AXE_WIDTHS = [375, 1280]

# mdBook shows the sidebar by default from this width up.
SIDEBAR_SHOWN_FROM = 1080

# The element that holds a page's own content (everything else is mdBook's frame).
CONTENT = "#mdbook-content main"

# Selector of everything that must stay inside the text column (U2).
CONTAINED_SELECTOR = "pre, figure, .tabs, .tab-list, blockquote, details, .table-wrapper, img, pre.mermaid svg"

_SUMMARY_ENTRY = re.compile(r"^\s*(?:[-*]\s+)?\[(?P<label>[^\]]+)\]\((?P<path>[^)]+)\)\s*$")


def read_summary() -> list[tuple[str, str]]:
    """The pages of the book in reading order, as (label, URL path), from docs/SUMMARY.md."""
    pages = []
    for line in (REPO_ROOT / "docs" / "SUMMARY.md").read_text().split("\n"):
        entry = _SUMMARY_ENTRY.match(line)
        if entry:
            pages.append((entry["label"], posixpath.splitext(entry["path"])[0] + ".html"))
    return pages


def discover_pages() -> list[str]:
    """Return the URL path of every page of the book ('index.html' is the home page).

    The list comes from docs/SUMMARY.md, and every page in it must have been built: a missing
    page is an error here, never a silently skipped test.
    """
    if not BOOK_DIR.is_dir():
        raise RuntimeError(f"{BOOK_DIR} does not exist. Run `make build` first (or use `make test-ui`).")
    paths = [path for _, path in read_summary()]
    if not paths:
        raise RuntimeError("docs/SUMMARY.md lists no pages.")
    missing = [path for path in paths if not (BOOK_DIR / path).is_file()]
    if missing:
        raise RuntimeError(f"Listed in docs/SUMMARY.md but not built in {BOOK_DIR}: {missing}. Run `make build`.")
    return paths


def built_pages() -> set[str]:
    """Every chapter page that mdBook wrote to book/ (not its helper pages)."""
    helpers = {"404.html", "print.html", "toc.html"}
    pages = set()
    for file in BOOK_DIR.rglob("*.html"):
        path = file.relative_to(BOOK_DIR).as_posix()
        if path not in helpers:
            pages.add(path)
    return pages


def pages_containing(pages: list[str], marker: str) -> list[str]:
    """The pages whose built HTML contains `marker`.

    Found in the built pages themselves, so a lesson that gets its first answer or diagram is tested
    without anyone remembering to list it. Code that shows HTML is escaped (`&lt;details`), so it never matches.
    """
    return [path for path in pages if marker in (BOOK_DIR / path).read_text(encoding="utf-8")]


def page_id(path: str) -> str:
    """A readable, file-system-safe name for a page ('ch00/01-x.html' becomes 'ch00__01-x')."""
    return path.removesuffix(".html").strip("/").replace("/", "__") or "index"


class _BookHandler(http.server.SimpleHTTPRequestHandler):
    """Serves book/ under SITE_PATH, and 404.html for anything else, as GitHub Pages does."""

    def translate_path(self, path: str) -> str:
        path = urlparse(path).path
        if not path.startswith(SITE_PATH):
            return str(BOOK_DIR / "does-not-exist")
        return super().translate_path("/" + path[len(SITE_PATH) :])

    def send_error(self, code, message=None, explain=None):
        if code != 404:
            return super().send_error(code, message, explain)
        body = (BOOK_DIR / "404.html").read_bytes()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # keep the test output readable
        pass


def start_server() -> tuple[str, http.server.ThreadingHTTPServer | None]:
    """Serve book/ on a free local port, or use BASE_URL when it is set.

    Returns (base_url_with_trailing_slash, server_or_None).
    """
    base_url = os.environ.get("BASE_URL")
    if base_url:
        return base_url.rstrip("/") + "/", None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), lambda *args: _BookHandler(*args, directory=str(BOOK_DIR)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_address[1]}{SITE_PATH}", server


def new_context(browser: Browser, width: int, scheme: str, **options) -> BrowserContext:
    """A fresh browser context for one viewport width and color scheme."""
    return browser.new_context(
        viewport={"width": width, "height": 800},
        color_scheme=scheme,
        reduced_motion="reduce",
        **options,
    )


# One JavaScript function that measures a loaded page (U1, U2, U3).
SURVEY_JS = (
    """
([content, selector]) => {
  const doc = document.documentElement;
  const inner = document.querySelector(content);
  const box = inner.getBoundingClientRect();
  const style = getComputedStyle(inner);
  const left = box.left + parseFloat(style.paddingLeft) + parseFloat(style.borderLeftWidth);
  const right = box.right - parseFloat(style.paddingRight) - parseFloat(style.borderRightWidth);

  const name = (el) => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
    (el.classList.length ? '.' + [...el.classList].slice(0, 2).join('.') : '');
  const scrollsSideways = (el) => {
    const overflow = getComputedStyle(el).overflowX;
    return (overflow === 'auto' || overflow === 'scroll') && el.scrollWidth > el.clientWidth + 1;
  };
  // An element inside a sideways-scrollable ancestor is judged by that ancestor.
  const judgedBy = (el) => {
    for (let a = el.parentElement; a && a !== inner; a = a.parentElement) {
      if (scrollsSideways(a)) return a;
    }
    return el;
  };

  const targets = [...inner.querySelectorAll(selector)];
  const outside = [];
  for (const el of targets) {
    const judge = judgedBy(el);
    const r = judge.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;  // hidden (e.g. an inactive tab)
    if (r.left < left - 1 || r.right > right + 1) {
      outside.push({ element: name(el), judgedBy: judge === el ? null : name(judge),
                     left: Math.round(r.left), right: Math.round(r.right),
                     columnLeft: Math.round(left), columnRight: Math.round(right) });
    }
  }

  // Content that is wider than its box must scroll, never be cut off silently.
  const clipped = [];
  for (const el of inner.querySelectorAll('*')) {
    if (el.clientWidth === 0 || el.scrollWidth <= el.clientWidth + 1) continue;
    const overflow = getComputedStyle(el).overflowX;
    if (overflow === 'hidden' || overflow === 'clip') {
      clipped.push({ element: name(el), scrollWidth: el.scrollWidth, clientWidth: el.clientWidth, overflowX: overflow });
    }
  }
  const codeBlocksThatDoNotScroll = [];
  for (const code of inner.querySelectorAll('pre > code')) {
    if (code.scrollWidth > code.clientWidth + 1) {
      const overflow = getComputedStyle(code).overflowX;
      if (overflow !== 'auto' && overflow !== 'scroll') {
        codeBlocksThatDoNotScroll.push({ element: name(code), overflowX: overflow });
      }
    }
  }

  // A diagram that was drawn while its answer was closed can end up with no size when the answer opens.
  const emptyDiagrams = [...inner.querySelectorAll('pre.mermaid svg')]
    .filter((svg) => { const r = svg.getBoundingClientRect(); return r.width === 0 || r.height === 0; })
    .map(name);

  // mdBook lets the text area (#mdbook-content) scroll sideways, so something wider than the column
  // does not widen the document: the page would still look fine to a check of the document alone.
  const area = inner.closest('#mdbook-content');

  return { scrollWidth: doc.scrollWidth, clientWidth: doc.clientWidth,
           areaScrollWidth: area.scrollWidth, areaClientWidth: area.clientWidth, outside, clipped,
           codeBlocksThatDoNotScroll, emptyDiagrams };
}
"""
)


@dataclass
class Survey:
    """What one page looks like at one viewport width and color scheme."""

    scroll_width: int
    client_width: int
    area_scroll_width: int  # the text area, which mdBook lets scroll sideways on its own
    area_client_width: int
    outside: list[dict]
    clipped: list[dict]
    code_blocks_that_do_not_scroll: list[dict]
    empty_diagrams: list[str]  # drawn diagrams with no size (only meaningful when every answer is open)
    problems: list[str]  # console errors, uncaught errors, failed or >=400 same-origin requests
    axe_violations: list[dict] | None  # axe-core violations, or None at widths where axe is not run


@dataclass
class Tab:
    """One browser page plus a record of what happened while it loaded."""

    page: Page
    base_url: str
    width: int = 0
    events: list[str] = field(default_factory=list)
    surveys: dict[tuple[str, bool], Survey] = field(default_factory=dict)

    def __post_init__(self) -> None:
        origin = urlparse(self.base_url).netloc
        self.page.on("console", lambda m: self.events.append(f"console error: {m.text}") if m.type == "error" else None)
        self.page.on("pageerror", lambda e: self.events.append(f"uncaught error: {e}"))
        self.page.on(
            "requestfailed",
            lambda r: self.events.append(f"request failed: {r.url} ({r.failure})") if urlparse(r.url).netloc == origin else None,
        )
        self.page.on(
            "response",
            lambda r: self.events.append(f"HTTP {r.status}: {r.url}") if r.status >= 400 and urlparse(r.url).netloc == origin else None,
        )

    def visit(self, path: str, open_details: bool = False) -> None:
        """Open a page fresh and wait until it has finished drawing.

        With open_details, every <details> on the page (answers and the questions around them, nested ones
        included) is opened, as a reader who wants to see all the answers would do.
        """
        self.events.clear()
        self.page.goto(self.base_url + path, wait_until="load")
        self.page.evaluate("document.fonts.ready.then(() => true)")
        # mdBook fills the sidebar with a script; wait for it so the page is measured as readers see it.
        self.page.wait_for_selector("#mdbook-sidebar .chapter a", state="attached", timeout=10_000)
        if open_details:
            self.page.evaluate("document.querySelectorAll('details').forEach((d) => { d.open = true; })")
            self.page.evaluate("new Promise((done) => requestAnimationFrame(() => requestAnimationFrame(done)))")
        # Let animations finish, so measurements (and axe's color checks) never see a half-faded state.
        self.page.wait_for_function(
            "document.getAnimations().every(a => a.playState !== 'running' || a.effect.getComputedTiming().iterations === Infinity)",
            timeout=5_000,
        )
        if self.page.evaluate("!!document.querySelector('.mermaid')"):
            try:
                self.page.wait_for_function(
                    "[...document.querySelectorAll('pre.mermaid')].every(diagram => diagram.querySelector('svg'))",
                    timeout=20_000,
                )
            except Exception as error:
                raise AssertionError(f"The diagram on '{path}' did not render.") from error

    def survey(self, path: str, open_details: bool = False) -> Survey:
        """Load a page once (closed, or with every answer opened) and measure it; later calls reuse the result."""
        key = (path, open_details)
        if key not in self.surveys:
            self.visit(path, open_details)
            raw = self.page.evaluate(SURVEY_JS, [CONTENT, CONTAINED_SELECTOR])
            self.surveys[key] = Survey(
                scroll_width=raw["scrollWidth"],
                client_width=raw["clientWidth"],
                area_scroll_width=raw["areaScrollWidth"],
                area_client_width=raw["areaClientWidth"],
                outside=raw["outside"],
                clipped=raw["clipped"],
                code_blocks_that_do_not_scroll=raw["codeBlocksThatDoNotScroll"],
                empty_diagrams=raw["emptyDiagrams"],
                problems=list(self.events),
                axe_violations=Axe().run(self.page).response["violations"] if self.width in AXE_WIDTHS else None,
            )
        return self.surveys[key]


# ------------------------------------------------------- parallel scheduling --

_VIEWPORT_ID = re.compile(r"[-\[](\d{3,4})-(light|dark)\]$")
_SCHEME_ONLY_ID = re.compile(r"\[(light|dark)\]$")


def _scope_of(nodeid: str) -> str:
    """The group of tests that should run on one worker, so they can share loaded pages.

    A test id ends in the page, the width and the color scheme (for example
    "[index-375-light]", or "[conventions-open-375-light]" for the pass with every answer opened). Everything measured at one width and scheme shares one browser tab
    that remembers each page it has loaded, so all of those tests go to the same worker: a page
    is then loaded once, not once per check. Checks that are not tied to a viewport form one
    group per check.
    """
    viewport = _VIEWPORT_ID.search(nodeid)
    if viewport:
        # The pass with every answer opened is as large as the closed one, so it gets its own groups
        # and the two can run on different workers.
        opened = "open-" if "-open-" in nodeid else ""
        return f"{opened}{viewport.group(1)}-{viewport.group(2)}"
    scheme_only = _SCHEME_ONLY_ID.search(nodeid)
    if scheme_only:  # the checks that are made at 320px and named only by color scheme
        return f"320-{scheme_only.group(1)}"
    return nodeid.split("::")[-1].split("[")[0]


@pytest.hookimpl(optionalhook=True)
def pytest_xdist_make_scheduler(config, log):
    """Group tests by viewport when they run in parallel with pytest-xdist.

    xdist's own `--dist loadgroup` is not used: with pytest 9.2 and pytest-xdist 3.8 it silently
    ignores the xdist_group marks, which put every test on a worker of its own.
    """
    from xdist.scheduler import LoadScopeScheduling

    class ByViewport(LoadScopeScheduling):
        def _split_scope(self, nodeid: str) -> str:
            return _scope_of(nodeid)

    return ByViewport(config, log)


# ------------------------------------------------------------ time report --

# Seconds spent per check (setup, call and teardown together) and how many tests ran. It helps
# to see where the time goes, locally and in CI, before deciding what to speed up.
_TIME_BY_CHECK: dict[str, list[float]] = {}


def pytest_runtest_logreport(report) -> None:
    check = report.nodeid.split("::")[-1].split("[")[0]
    entry = _TIME_BY_CHECK.setdefault(check, [0.0, 0.0])
    entry[0] += report.duration
    if report.when == "call":
        entry[1] += 1


def pytest_terminal_summary(terminalreporter) -> None:
    if not _TIME_BY_CHECK:
        return
    total = sum(seconds for seconds, _ in _TIME_BY_CHECK.values())
    terminalreporter.section("time spent per check (all workers added together)")
    for check, (seconds, count) in sorted(_TIME_BY_CHECK.items(), key=lambda item: -item[1][0]):
        terminalreporter.write_line(f"{seconds:8.1f} s  {int(count):5d} tests  {check}")
    terminalreporter.write_line(f"{total:8.1f} s  in total")


# ------------------------------------------------------ failure evidence --


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """When a browser test fails, save a screenshot of the page it was checking.

    The picture goes to artifacts/screenshots/failures/ (CI uploads that folder when a run
    fails). It is taken at the failing test's own width and color scheme. Taking it must never
    hide the real failure, so any error while doing so is ignored.
    """
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    tabs = item.funcargs.get("tabs")
    params = getattr(getattr(item, "callspec", None), "params", {})
    if tabs is None or "width" not in params or "scheme" not in params:
        return
    try:
        tab = tabs(params["width"], params["scheme"])
        if "path" in params:
            tab.visit(params["path"], open_details="-open-" in item.callspec.id)
        FAILURE_SHOTS.mkdir(parents=True, exist_ok=True)
        name = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.name)
        tab.page.screenshot(path=str(FAILURE_SHOTS / f"{name}.png"), full_page=True)
    except Exception:
        pass


# ---------------------------------------------------------------- fixtures --


@pytest.fixture(scope="session")
def base_url():
    url, server = start_server()
    yield url
    if server:
        server.shutdown()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        chromium = playwright.chromium.launch()
        yield chromium
        chromium.close()


@pytest.fixture(scope="session")
def tabs(browser, base_url):
    """Hands out one cached Tab per (width, scheme), so fonts and scripts load once per combination."""
    cache: dict[tuple[int, str], Tab] = {}

    def get(width: int, scheme: str) -> Tab:
        if (width, scheme) not in cache:
            context = new_context(browser, width, scheme)
            cache[(width, scheme)] = Tab(context.new_page(), base_url, width)
        return cache[(width, scheme)]

    yield get
    for tab in cache.values():
        tab.page.context.close()


# Every book page. Discovery fails loudly (rather than testing nothing) if book/ is missing or incomplete.
PAGES = discover_pages()

# The pages that have at least one question with an answer, and the pages that have a diagram.
DETAILS_PAGES = pages_containing(PAGES, "<details")
DIAGRAM_PAGES = pages_containing(PAGES, 'class="mermaid"')
