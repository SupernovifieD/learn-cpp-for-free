# Contributing to The C++ Book

Thank you for helping. This guide explains how to set up your computer, how to add a lesson or a chapter, and the rules that keep the book consistent. A new lesson should need only Markdown and C++ files: you never have to touch the stylesheet, the workflow or the scripts.

## Ground rules

- **Write everything yourself.** Do not copy or closely paraphrase text, examples or images from other books or websites. Check facts against primary sources such as cppreference.com, isocpp.org and the GCC, Clang and Microsoft documentation.
- **Keep it simple.** Plain Markdown, one stylesheet, no custom JavaScript, no third-party plugins and no theme overrides. The site must stay easy to move to another generator.
- **Never weaken a check** to make it pass. Fix the cause instead.

## Set up your computer

You need Python 3.11 or newer, `make`, Git and a C++ compiler. The example checker builds every program with both GCC and Clang, so install both if you can.

**macOS and Linux**

```bash
git clone https://github.com/SupernovifieD/learn-cpp-for-free.git
cd learn-cpp-for-free
make install
```

`make install` creates a virtual environment in `.venv`, installs the pinned dependencies and downloads the browser that the UI tests use.

**Windows (PowerShell)**

`make` is often missing on Windows, so run the commands directly. After the setup below, activate the virtual environment with `.venv\Scripts\Activate.ps1`, so that `python` in the table points at it.

```powershell
git clone https://github.com/SupernovifieD/learn-cpp-for-free.git
cd learn-cpp-for-free
py -3 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python -m playwright install chromium
```

| Task | `make` target | Command without `make` |
| --- | --- | --- |
| Preview the book | `make serve` | `python -m mkdocs serve` |
| Build the site | `make build` | `python -m mkdocs build --strict` |
| Lint the content | `make lint` | `python scripts/lint_content.py` |
| Check the examples | `make examples` | `python scripts/check_examples.py` |
| Check formatting | `make format-check` | `clang-format --dry-run --Werror` on every `.cpp` file in `examples/` |
| Browser tests | `make test-ui` | `python -m pytest tests/ui -n 2 --dist loadscope` |

**A note about GCC on macOS.** The `g++` command on macOS is Apple's Clang. The example checker detects this, does not count it as GCC and prints a warning. To check with real GCC, install it (for example with Homebrew) and point the checker at it: `GXX=g++-15 make examples`. CI always checks with real GCC.

## Daily workflow

1. Create a branch from `main`.
2. Run `make serve` and edit files. The browser reloads when you save.
3. Run `make check` before you commit. It runs, in order: the content lint, the example check, the format check, the strict build and the browser tests. CI runs the same commands.
4. Open a pull request. The checklist in the pull request template mirrors this guide.

Material for MkDocs prints a notice about its end of life at the start of every build. That is expected, and it does not fail the build.

`make format` reformats the C++ examples with the pinned `clang-format`, so everyone formats the same way. `make screenshots` saves pictures of every page to `artifacts/screenshots/` for the visual review described below.

## Add a lesson in 5 steps

Suppose you are adding lesson 0.14, "Example lesson".

1. **Copy the template.** Copy `templates/lesson.md` to `docs/ch00-getting-started/14-example-lesson.md`. Lesson files are named `NN-slug.md`, with a two-digit number and a kebab-case slug. Fill in the `description` (one sentence, at most 160 characters) and the title. The first heading must be the label you will use in the navigation, such as `# 0.14 Example lesson`. Then write the lesson: replace every placeholder with real text and delete every comment from the template. `make lint` rejects a page that still contains template text.
2. **Write the example programs.** Put each complete program in `examples/ch00/14-example-lesson.cpp` and its exact expected output in `examples/ch00/14-example-lesson.out`. Run `make format` and then `make examples`, and fix everything they report. If the output differs between machines, leave out the `.out` file and show an example output in the lesson.
3. **Include the programs in the lesson.** Never paste a complete program into a lesson. Include the file, and its output, like this:

    ````markdown
    ```cpp title="example-lesson.cpp"
    --8<-- "examples/ch00/14-example-lesson.cpp"
    ```

    ```text title="Output"
    --8<-- "examples/ch00/14-example-lesson.out"
    ```
    ````

4. **Add the page to the navigation.** In `mkdocs.yml`, add a line under the chapter in `nav:` with the same label as the lesson's first heading:

    ```yaml
    - "0.14 Example lesson": ch00-getting-started/14-example-lesson.md
    ```

    Also add the lesson to the list in the chapter's `index.md`.
5. **Check, review and commit.** Run `make check`. Then run `make screenshots`, look at the pictures of your page (see the visual checklist below), and commit with a message such as `docs(ch00): add lesson 0.14`.

## Add a chapter

1. Create the folder `docs/chNN-slug/` with a two-digit chapter number.
2. Copy `templates/chapter-index.md` to `docs/chNN-slug/index.md` and fill it in.
3. Add the chapter to `nav:` in `mkdocs.yml`. The chapter's `index.md` comes first, with no label, followed by its lessons:

    ```yaml
    - "1. Chapter title":
        - ch01-slug/index.md
        - "1.1 First lesson": ch01-slug/01-first-lesson.md
    ```

4. Add the chapter to the contents list on the home page (`docs/index.md`).
5. Create `examples/ch01/` for the chapter's programs, and then add the lessons as described above.

## Rules for examples

- **Names.** `examples/chNN/NN-slug.cpp`, where `NN` is the number of the lesson that first uses the program.
- **Output.** The exact expected standard output goes in `NN-slug.out`. If the program reads input, put it in `NN-slug.in`.
- **Programs that must fail.** Name them `NN-slug.fail.cpp`. The first line must be `// expect-fail: <one-line reason>`. An optional second line, `// passes-without: <flag> [<flag> ...]`, makes the checker also prove that the file builds once those flags are removed, which shows that the failure comes from the flags the book teaches.
- **Every example is used.** Each file in `examples/` must be included by at least one page, or `make lint` fails.
- **Formatting.** 4-space indent, braces on their own line, at most 80 columns, one statement per line, brace initialization, `"\n"` instead of `std::endl`. `make format` applies the rules from `.clang-format`.
- **The strict flags.** `examples/flags-gcc-clang.txt` holds the one line of compiler flags that CI uses and that lesson 0.11 shows. Change it only on purpose, because it changes what the book promises.

## Writing style

- Write to "you", in a friendly, direct and precise tone, in American English.
- Keep paragraphs to four sentences or fewer, with one idea per section.
- Bold a term where you define it, and use it consistently afterwards.
- Never use "simply", "just", "obviously" or "easy".
- Put identifiers, file names and commands in backticks, UI labels in bold (**File > New > Project**) and keys like `++ctrl+f5++`.
- Point forward ("You will learn what `std::cout` is in Chapter 1") instead of over-explaining.
- Phrase facts that change, such as versions and menu names, so that they age well, and link the official page.
- No raw HTML and no emoji in pages.
- Shell commands go in `bash` (or `powershell`) blocks without a `$` prompt, so the copy button copies a runnable command.

Each lesson has this shape: front matter with a `description`, the heading, an opening paragraph, sections in sentence case, an optional "Check your understanding" collapsible, a `## Summary` with 3 to 6 bullets, and an optional `## Further reading` that links primary sources over https. Do not write previous and next links by hand, because the page footer provides them.

## Callouts

Use only these types, and use them sparingly: never two callouts back to back, about one per 300 words at most, and never put a complete program inside one.

| Type | Use it for |
| --- | --- |
| `note` | Useful context that is not essential |
| `tip` | A handier way to do something |
| `warning` | A common mistake or a surprise |
| `danger` | Something that can lose data or damage a setup (rare) |
| `best-practice` | A habit professionals follow, with the reason |
| `key-insight` | The idea that makes a topic fall into place |
| `advanced` | An aside for readers who want more depth |
| `question` and `success` | The collapsible question and its answer |

The page "Conventions used in this book" shows every type.

## Tabs

When instructions depend on the reader's system or tools, use tabs, and use only these two sets of labels, spelled exactly like this:

- Operating systems: `Windows`, `macOS`, `Linux`
- Toolchains: `Visual Studio`, `VS Code`, `Command line`

Every tab in a set holds the same kind of information in the same order, with bold labels such as **Install:** and **Check:**. The linter rejects other labels and mixed sets.

## Diagrams

Use Mermaid, top to bottom (`flowchart TD`), with short node labels and no custom colors. Put one plain sentence that describes the diagram before it, for screen-reader users. Keep each row to at most two nodes: a wider diagram is scaled down on a phone until its text is too small, and the UI test for the diagram fails when text falls below 12px.

## Tables

A table wider than the page scrolls inside its frame, but readers on phones should not have to scroll. Keep tables to three columns or fewer with short cells, and split a wide table into two. Material's own markup for scrolling tables cannot be made keyboard-focusable without a template override, which this book avoids on purpose (see `tests/ui/axe_allowlist.json`).

## Browser tests and visual review

`make test-ui` builds the site and opens every page in a headless browser at nine widths (320 to 1920 pixels) in light and dark mode. It checks, among other things, that:

- the page never scrolls sideways and nothing sticks out of the text column,
- long code lines scroll inside their own block,
- there are no console errors or failed requests,
- axe-core finds no serious or critical accessibility problems,
- every page has one `h1` and no skipped heading levels,
- the theme toggle, the previous and next links, the search and the Mermaid diagram work.

When a check fails, the test run saves a screenshot of the failing page to `artifacts/screenshots/failures/`, and CI uploads that folder. Optional settings: `UI_WORKERS` sets how many browsers run in parallel (`make test-ui UI_WORKERS=4`, default 2), `BASE_URL` tests a published site instead of the local build, and `MERMAID_JS` points to a local copy of Material's Mermaid script if you cannot reach its CDN.

Automated checks do not see everything, so look at the screenshots of your page (375 and 1280 pixels wide in both color schemes, plus 320 for pages with tabs, tables or diagrams) and check that:

1. callout icons are centered on the title and custom callouts match the built-in ones;
2. the copy button never covers code, and code titles line up with the block edges;
3. output blocks look different from code but line up with it;
4. tab labels sit on one line and nothing is clipped on a phone;
5. long sidebar titles wrap with a clean indent and the current page is clearly highlighted;
6. the previous and next titles at the bottom do not overlap their arrows;
7. tables have an aligned header row and padded cells;
8. there is no doubled or collapsed spacing, for example between a heading and a callout;
9. dark mode has no white boxes and no dark-on-dark text;
10. the header never collides at 320 to 414 pixels;
11. rendered keys do not disturb the line height;
12. no text is smaller than 12px, and inline code is legible in both color schemes.

## Content checklist

Before you open a pull request, check that:

1. the wording is original, with nothing copied or closely paraphrased;
2. every fact that can change was checked against a primary source today;
3. the lesson covers what it promises and does not teach later chapters in depth;
4. every complete program is an included, checked example;
5. each term is bolded once where it is defined, and used consistently afterwards;
6. callouts have the right type and are not stacked or overused;
7. tabs use the exact label sets;
8. the length is reasonable and paragraphs have four sentences or fewer;
9. a summary is present, and further reading uses primary sources over https;
10. a beginner could follow every instruction without guessing.

## Commits and pull requests

Use Conventional Commits, `type(scope): description`, with one coherent change per commit. Common types are `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `build`, `ci` and `chore`. Examples: `docs(ch00): add lesson 0.14`, `fix(theme): keep icons aligned in callouts`.

Do not commit the virtual environment, the `site/` folder, screenshots, caches or secrets. Open a pull request against `main` and fill in the checklist. Every check must be green before it can be merged.

Found a factual mistake? [Open an issue](https://github.com/SupernovifieD/learn-cpp-for-free/issues/new?template=content-error.md) or use the **Edit this page** button on the page.
