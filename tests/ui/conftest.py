"""Shared helpers and fixtures for the browser tests (layout, accessibility, behavior).

The tests drive headless Chromium against the built site in site/ (run
`make build` first, or use `make test-ui`, which builds for you).

Environment variables (all optional):
  BASE_URL    Test an already published site, e.g. the live GitHub Pages URL,
              instead of serving the local site/ directory. Pages are still
              discovered from the local site/ build.
  MERMAID_JS  Path to a local copy of Material's Mermaid bundle. Material loads
              Mermaid from a CDN; set this to run without reaching the CDN.

This module also holds the small browser helpers that tests/ui/screenshots.py
reuses, so both always open pages the same way.
"""

from __future__ import annotations

import functools
import http.server
import os
import re
import threading
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_DIR = REPO_ROOT / "site"
FAILURE_SHOTS = REPO_ROOT / "artifacts" / "screenshots" / "failures"

# Viewport widths from the UI quality bar (height is always 800).
WIDTHS = [320, 360, 375, 414, 768, 1024, 1280, 1440, 1920]
SCHEMES = ["light", "dark"]

# Widths at which axe-core also checks every page (U5). It runs on the same page load that the
# layout checks use, so the page is not loaded a second time.
AXE_WIDTHS = [375, 1280]

# Sub-folders of site/ that hold assets, not book pages.
NON_PAGE_DIRS = {"assets", "search"}

# Material draws Mermaid diagrams inside a *closed* shadow root, which no test
# can look into. Forcing shadow roots open is the only way to check that an
# <svg> was really drawn. This changes nothing about how pages look.
OPEN_SHADOW_ROOTS_JS = """
const attach = Element.prototype.attachShadow;
Element.prototype.attachShadow = function (init) {
  return attach.call(this, { ...init, mode: 'open' });
};
"""

# Selector of everything that must stay inside the text column (U2).
CONTAINED_SELECTOR = (
    "pre, .highlight, .tabbed-set, .admonition, details, "
    ".md-typeset__scrollwrap, img, .md-button, blockquote"
)


def discover_pages() -> list[str]:
    """Return the URL path of every book page found in site/ ('' is the home page)."""
    if not SITE_DIR.is_dir():
        raise RuntimeError(f"{SITE_DIR} does not exist. Run `make build` first (or use `make test-ui`).")
    paths = []
    for index in sorted(SITE_DIR.rglob("index.html")):
        folder = index.parent.relative_to(SITE_DIR)
        if folder.parts and folder.parts[0] in NON_PAGE_DIRS:
            continue
        paths.append("" if not folder.parts else folder.as_posix() + "/")
    if not paths:
        raise RuntimeError(f"No pages found in {SITE_DIR}. Run `make build` first.")
    return paths


def page_id(path: str) -> str:
    """A readable, file-system-safe name for a page ('' becomes 'index')."""
    return path.strip("/").replace("/", "__") or "index"


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):  # keep the test output readable
        pass


def start_server() -> tuple[str, http.server.ThreadingHTTPServer | None]:
    """Serve site/ on a free local port, or use BASE_URL when it is set.

    Returns (base_url_with_trailing_slash, server_or_None).
    """
    base_url = os.environ.get("BASE_URL")
    if base_url:
        return base_url.rstrip("/") + "/", None
    handler = functools.partial(_QuietHandler, directory=str(SITE_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_address[1]}/", server


def _stub_github_api(route) -> None:
    """Answer Material's repository lookups without touching api.github.com.

    The header asks GitHub for the repository's stars, forks and latest
    release. Live answers would make the tests depend on the network and on
    GitHub's rate limits (and, while the repository has no release, GitHub
    answers 404, which the browser logs as a console error). The stub returns
    all three facts, which is the widest the header can ever be.
    """
    if route.request.url.endswith("/releases/latest"):
        body = '{"tag_name": "v0.1.0"}'
    else:
        body = '{"stargazers_count": 12, "forks_count": 3}'
    route.fulfill(status=200, content_type="application/json", body=body)


# Files already downloaded in this test run, keyed by URL: the web fonts and Material's Mermaid
# script. Every browser context starts with an empty cache and the pages are measured hundreds
# of times, so without this each visit would download the same files again.
_DOWNLOAD_CACHE: dict[str, tuple[dict[str, str], bytes]] = {}


def _serve_from_memory(route) -> None:
    """Download each file once, then answer every later request from memory.

    The pages are measured with the real fonts and the real Mermaid script (text width decides
    where lines wrap, and the diagram must really draw), so nothing is blocked or replaced, only
    remembered. The bytes are exactly what the server sent.
    """
    url = route.request.url
    if url not in _DOWNLOAD_CACHE:
        response = route.fetch()
        if response.status != 200:
            route.fulfill(response=response)
            return
        skipped = {"content-encoding", "content-length", "transfer-encoding"}
        headers = {k: v for k, v in response.headers.items() if k.lower() not in skipped}
        _DOWNLOAD_CACHE[url] = (headers, response.body())
    headers, body = _DOWNLOAD_CACHE[url]
    route.fulfill(status=200, headers=headers, body=body)


def new_context(browser: Browser, width: int, scheme: str) -> BrowserContext:
    """A fresh browser context for one viewport width and color scheme."""
    context = browser.new_context(
        viewport={"width": width, "height": 800},
        color_scheme=scheme,
        reduced_motion="reduce",
    )
    context.add_init_script(OPEN_SHADOW_ROOTS_JS)
    context.route("https://api.github.com/**", _stub_github_api)
    context.route("https://fonts.googleapis.com/**", _serve_from_memory)
    context.route("https://fonts.gstatic.com/**", _serve_from_memory)
    # Registered before the MERMAID_JS override below, which must win when it is set.
    context.route("https://unpkg.com/**/mermaid.min.js", _serve_from_memory)
    mermaid_js = os.environ.get("MERMAID_JS")
    if mermaid_js:
        context.route(
            "**/mermaid.min.js",
            lambda route: route.fulfill(path=mermaid_js, content_type="application/javascript"),
        )
    return context


# One JavaScript function that measures a loaded page (U1, U2, U3).
SURVEY_JS = (
    """
(selector) => {
  const doc = document.documentElement;
  const inner = document.querySelector('.md-content__inner');
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
  for (const host of inner.querySelectorAll('.mermaid')) {
    const svg = host.shadowRoot && host.shadowRoot.querySelector('svg');
    if (svg) targets.push(svg);
  }
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

  return { scrollWidth: doc.scrollWidth, clientWidth: doc.clientWidth, outside, clipped,
           codeBlocksThatDoNotScroll };
}
"""
)


@dataclass
class Survey:
    """What one page looks like at one viewport width and color scheme."""

    scroll_width: int
    client_width: int
    outside: list[dict]
    clipped: list[dict]
    code_blocks_that_do_not_scroll: list[dict]
    problems: list[str]  # console errors, uncaught errors, failed or >=400 same-origin requests
    axe_violations: list[dict] | None  # axe-core violations, or None at widths where axe is not run


@dataclass
class Tab:
    """One browser page plus a record of what happened while it loaded."""

    page: Page
    base_url: str
    width: int = 0
    events: list[str] = field(default_factory=list)
    surveys: dict[str, Survey] = field(default_factory=dict)

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

    def visit(self, path: str) -> None:
        """Open a page fresh and wait until it has finished drawing."""
        self.events.clear()
        self.page.goto(self.base_url + path, wait_until="load")
        self.page.evaluate("document.fonts.ready.then(() => true)")
        # Material asks GitHub for repository facts after load; wait for them so a late error is caught.
        self.page.wait_for_selector(".md-source__fact--stars", state="attached", timeout=10_000)
        # Let fade-in animations finish, so measurements (and axe's color checks) never see a half-faded state.
        self.page.wait_for_function(
            "document.getAnimations().every(a => a.playState !== 'running' || a.effect.getComputedTiming().iterations === Infinity)",
            timeout=5_000,
        )
        has_diagram = self.page.evaluate("!!document.querySelector('.mermaid')")
        if has_diagram:
            try:
                self.page.wait_for_function(
                    "!document.querySelector('pre.mermaid') && [...document.querySelectorAll('.mermaid')]"
                    ".every(h => h.shadowRoot && h.shadowRoot.querySelector('svg'))",
                    timeout=20_000,
                )
            except Exception as error:
                raise AssertionError(
                    f"The diagram on '{path or 'index'}' did not render. Material loads Mermaid from a CDN: "
                    "check your network, or point MERMAID_JS at a local copy of the bundle."
                ) from error

    def survey(self, path: str) -> Survey:
        """Load a page once and measure it; later calls reuse the result."""
        if path not in self.surveys:
            self.visit(path)
            raw = self.page.evaluate(SURVEY_JS, CONTAINED_SELECTOR)
            self.surveys[path] = Survey(
                scroll_width=raw["scrollWidth"],
                client_width=raw["clientWidth"],
                outside=raw["outside"],
                clipped=raw["clipped"],
                code_blocks_that_do_not_scroll=raw["codeBlocksThatDoNotScroll"],
                problems=list(self.events),
                axe_violations=Axe().run(self.page).response["violations"] if self.width in AXE_WIDTHS else None,
            )
        return self.surveys[path]


# ------------------------------------------------------- parallel scheduling --

_VIEWPORT_ID = re.compile(r"[-\[](\d{3,4})-(light|dark)\]$")
_SCHEME_ONLY_ID = re.compile(r"\[(light|dark)\]$")


def _scope_of(nodeid: str) -> str:
    """The group of tests that should run on one worker, so they can share loaded pages.

    A test id ends in the page, the width and the color scheme (for example
    "[index-375-light]"). Everything measured at one width and scheme shares one browser tab
    that remembers each page it has loaded, so all of those tests go to the same worker: a page
    is then loaded once, not once per check. Checks that are not tied to a viewport form one
    group per check.
    """
    viewport = _VIEWPORT_ID.search(nodeid)
    if viewport:
        return f"{viewport.group(1)}-{viewport.group(2)}"
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
            tab.visit(params["path"])
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


# Every book page. Discovery fails loudly (rather than testing nothing) if site/ is missing.
PAGES = discover_pages()
