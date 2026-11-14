# Contributing to The C++ Book

Thank you for helping. This guide explains how to set up your computer, how to add a lesson or a chapter, and the rules that keep the book consistent. A new lesson should need only Markdown and C++ files: you never have to touch the theme, the workflow or the scripts.

## Ground rules

- **Write everything yourself.** Do not copy or closely paraphrase text, examples or images from other books or websites. Check facts against primary sources such as cppreference.com, isocpp.org and the GCC, Clang and Microsoft documentation.
- **Keep it simple.** Plain Markdown on top of mdBook's own look. The only additions are one small stylesheet and script in `theme/` and one preprocessor, `scripts/mdbook_cppbook.py`. No copies of mdBook's templates, and no other plugins unless a lesson cannot be written without them.
- **Never weaken a check** to make it pass. Fix the cause instead.

## Set up your computer

You need Python 3.11 or newer, `make`, Git and a C++ compiler. The example checker builds every program with both GCC and Clang, so install both if you can. You do not need Rust: mdBook is a single program that `make install` downloads.

**macOS and Linux**

```bash
git clone https://github.com/SupernovifieD/learn-cpp-for-free.git
cd learn-cpp-for-free
make install
```

`make install` downloads mdBook and mdbook-mermaid at the versions pinned in `scripts/install_tools.py` into `.tools/` (it checks each download against a SHA-256), creates a virtual environment in `.venv` for the test tools, installs the pinned packages and downloads the browser that the UI tests use.

**Windows (PowerShell)**

`make` is often missing on Windows, so run the commands directly. After the setup below, activate the virtual environment with `.venv\Scripts\Activate.ps1`, so that `python` in the table points at it, and put the tools on your path with `$env:PATH = "$PWD\.tools\bin;$env:PATH"`.

```powershell
git clone https://github.com/SupernovifieD/learn-cpp-for-free.git
cd learn-cpp-for-free
py -3 scripts/install_tools.py
py -3 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python -m playwright install chromium
```

| Task | `make` target | Command without `make` |
| --- | --- | --- |
| Preview the book | `make serve` | `mdbook serve` |
| Build the book | `make build` | `mdbook build` |
| Lint the content | `make lint` | `python scripts/lint_content.py` |
| Check the examples | `make examples` | `python scripts/check_examples.py` |
| Test the example checker | `make test-scripts` | `python -m pytest tests/scripts` |
| Check formatting | `make format-check` | `clang-format --dry-run --Werror` on every `.cpp` and `.h` file in `examples/` |
| Browser tests | `make test-ui` | `mdbook build`, then `python -m pytest tests/ui -n 2 --dist loadscope` |
| Screenshots | `make screenshots` | `mdbook build`, then `python tests/ui/screenshots.py` |

Two details of `mdbook build`: it prints a note that mdbook-mermaid was built against an earlier 0.5 release, which is expected, and it exits successfully even when an include names a missing file, so `make build` also fails when its log contains a `WARN` or `ERROR` line.

**A note about GCC on macOS.** The `g++` command on macOS is Apple's Clang. The example checker detects this, does not count it as GCC and prints a warning. To check with real GCC, install it (for example with Homebrew) and point the checker at it: `GXX=g++-15 make examples`. CI always checks with real GCC.

## Daily workflow

1. Create a branch from `main`.
2. Run `make serve` and edit files. The browser reloads when you save, also when you change a file in `examples/`.
3. Run `make check` before you commit. It runs, in order: the content lint, the tests of the example checker, the example check, the format check, the build and the browser tests. CI runs the same commands.
4. Open a pull request. The checklist in the pull request template mirrors this guide.

`make format` reformats the C++ examples with the pinned `clang-format`, so everyone formats the same way. `make screenshots` saves pictures of every page to `artifacts/screenshots/` for the visual review described below.

## Add a lesson in 5 steps

Suppose you are adding lesson 0.14, "Example lesson".

1. **Copy the template.** Copy `templates/lesson.md` to `docs/ch00-getting-started/14-example-lesson.md`. Lesson files are named `NN-slug.md`, with a two-digit number and a kebab-case slug. The first heading must be the label you will use in the table of contents, such as `# 0.14 Example lesson`. Pages have no front matter: the file starts with its heading. Then write the lesson: replace every placeholder with real text and delete every comment from the template. `make lint` rejects a page that still contains template text.
2. **Write the example programs.** Put each complete program in `examples/ch00/14-example-lesson.cpp` and its exact expected output in `examples/ch00/14-example-lesson.out`. Run `make format` and then `make examples`, and fix everything they report. If the output differs between machines, leave out the `.out` file and show an example output in the lesson.
3. **Include the programs in the lesson.** Never paste a complete program into a lesson. Include the file, and its output, with `{{#include}}`. The path is relative to the page, so from a lesson in `docs/ch00-getting-started/` it starts with `../../examples/`:

    ````markdown
    ```cpp title="example-lesson.cpp"
    {{#include ../../examples/ch00/14-example-lesson.cpp}}
    ```

    ```text title="Output"
    {{#include ../../examples/ch00/14-example-lesson.out}}
    ```
    ````

    The `title` is the label above the block: a file name is shown as "Filename: example-lesson.cpp", and any other title, such as `Output`, as written. An inline fragment of five lines or fewer may be written in the fence itself, with or without a title. Always give a fence a language (`cpp`, `bash`, `powershell`, `text`). A line of code that is too wide scrolls inside its block.
4. **Add the page to the table of contents.** In `docs/SUMMARY.md`, add a line under the chapter, indented by two spaces, with the same label as the lesson's first heading:

    ```markdown
    - [0.14 Example lesson](ch00-getting-started/14-example-lesson.md)
    ```

    Also add the lesson to the list in the chapter's `index.md`. Order in `SUMMARY.md` is the reading order and the order of the previous and next arrows.
5. **Check, review and commit.** Run `make check`. Then run `make serve` or `make screenshots`, look at your page (see the visual checklist below), and commit with a message such as `docs(ch00): add lesson 0.14`.

## Add a chapter

1. Create the folder `docs/chNN-slug/` with a two-digit chapter number.
2. Copy `templates/chapter-index.md` to `docs/chNN-slug/index.md` and fill it in.
3. Add the chapter to `docs/SUMMARY.md`. The chapter's `index.md` is the chapter's own entry, and its lessons are indented by two spaces under it:

    ```markdown
    - [1. Chapter title](ch01-slug/index.md)
      - [1.1 First lesson](ch01-slug/01-first-lesson.md)
    ```

4. Add the chapter to the contents list on the home page (`docs/index.md`).
5. Create `examples/ch01/` for the chapter's programs, and then add the lessons as described above.

## Rules for examples

- **Names.** `examples/chNN/NN-slug.cpp`, where `NN` is the number of the lesson that first uses the program.
- **Projects (programs with several files).** A program is either one file or a folder. A project is a folder such as `examples/ch02/08-two-files/` that holds the program's `.cpp` files and the `.h` headers they include, with one of the files named `main.cpp`. The checker compiles and links every `.cpp` file of the folder in one command. The folder is flat (no folders inside it), and a `.cpp` file inside it is never a program of its own. Headers are allowed only inside project folders, and they follow the same formatting rules as `.cpp` files.
- **Files that belong to a program** sit next to it, whether it is a file or a folder, never inside the project folder: `08-two-files.out` is the output of the folder `08-two-files/`. The exact expected standard output goes in `NN-slug.out`.
- **Programs that read input** have two more files. `NN-slug.in` holds what the reader types, one line for each press of the Enter key. `NN-slug.session` holds what the reader sees in the console: the program's output with the typed lines where they appear on the screen. For a program that prints `Enter a number: ` and then `Twice that is 14` after the reader types 7, the session is `Enter a number: 7` followed by `Twice that is 14` on the next line. The checker proves that removing each line of `.in`, in order, from where it appears in the session leaves exactly the program's output, so a wrong output line, a missing typed line and an input line that the session never shows are all errors. It cannot prove that the program really read every typed line, so keep the input short and say in the lesson what the reader types. A program has `.out` or `.session`, never both, and `.in` always goes with `.session`. Show a session in a block titled `Example session` (```` ```text title="Example session" ````) instead of `Output`, and write in the prose what the reader types ("Type 7 and press Enter").
- **Programs that must fail.** Name a file `NN-slug.fail.cpp` and a project folder `NN-slug.fail/`. The first line of the file (of `main.cpp` for a project) must be `// expect-fail: <one-line reason>`. An optional second line, `// passes-without: <flag> [<flag> ...]`, makes the checker also prove that the program builds once those flags are removed, which shows that the failure comes from the flags the book teaches. A failing program never runs, so it has no `.out`, `.in` or `.session` file. The checker only knows that the build failed, so check yourself that it fails for the reason you describe.
- **Every example is used.** Each file in `examples/` must be included by at least one page, or `make lint` fails. A lesson shows a project as one titled block per file (`title="main.cpp"`, `title="add.h"`): headers first, then the other `.cpp` files, then `main.cpp`, then the output.
- **Formatting.** 4-space indent, braces on their own line, at most 80 columns, one statement per line, brace initialization, `"\n"` instead of `std::endl`. `make format` applies the rules from `.clang-format` to every `.cpp` and `.h` file.
- **The strict flags.** `examples/flags-gcc-clang.txt` holds the one line of compiler flags that CI uses and that lesson 0.11 shows. Change it only on purpose, because it changes what the book promises.

## Writing style

- Write to "you", in a friendly, direct and precise tone, in American English.
- Keep paragraphs to four sentences or fewer, with one idea per section.
- Bold a term where you define it, and use it consistently afterwards.
- Never use "simply", "just", "obviously" or "easy".
- Put identifiers, file names and commands in backticks, UI labels in bold (**File > New > Project**) and keys in `<kbd>`, one element per key: `<kbd>Ctrl</kbd>+<kbd>F5</kbd>`.
- Point forward ("You will learn what `std::cout` is in Chapter 1") instead of over-explaining.
- Phrase facts that change, such as versions and menu names, so that they age well, and link the official page.
- No raw HTML and no emoji in pages. The only HTML allowed is `<details>`, `<summary>` and `<kbd>`, without attributes.
- Shell commands go in `bash` (or `powershell`) blocks without a `$` prompt, so the copy button copies a runnable command.

Each lesson has this shape: the heading, an opening paragraph, sections in sentence case, an optional "Check your understanding" collapsible, a `## Summary` with 3 to 6 bullets, and an optional `## Further reading` that links primary sources over https. Do not write previous and next links by hand, because the book provides the arrows. Links to other pages are relative `.md` links (`[Conventions](../conventions.md)`, optionally with `#heading-id`); the linter checks that the page and the heading exist.

## Callouts

A callout is a block quote whose first line names its kind in capitals:

```markdown
> [!TIP]
> Type each example yourself instead of pasting it.
```

Use only these kinds, and use them sparingly: never two callouts back to back, about one per 300 words at most, and never put a complete program inside one.

| Kind | Use it for |
| --- | --- |
| `[!NOTE]` | Useful context that is not essential |
| `[!TIP]` | A handier way to do something |
| `[!WARNING]` | A common mistake or a surprise |
| `[!DANGER]` | Something that can lose data or damage a setup (rare) |
| `[!BEST-PRACTICE]` | A habit professionals follow, with the reason |
| `[!KEY-INSIGHT]` | The idea that makes a topic fall into place |
| `[!ADVANCED]` | An aside for readers who want more depth |

The first three are mdBook's own. `scripts/mdbook_cppbook.py` renders the other four with the same markup. A question with its answer is a pair of nested `<details>` elements, which start closed. Keep the empty lines and do not indent anything:

```markdown
<details>
<summary>Check your understanding</summary>

The question.

<details>
<summary>Answer</summary>

The answer.

</details>

</details>
```

The page "Conventions used in this book" shows every kind.

## Tabs

When instructions depend on the reader's system or tools, use tabs, and use only these two sets of labels, spelled exactly like this:

- Operating systems: `Windows`, `macOS`, `Linux`
- Toolchains: `Visual Studio`, `VS Code`, `Command line`

Every tab in a set holds the same kind of information in the same order, with bold labels such as **Install:** and **Check:**. Every marker stands alone at the start of a line, with an empty line after `{{#tab ...}}`:

```markdown
{{#tabs}}
{{#tab Windows}}

**Install:** Text for Windows.

{{#endtab}}
{{#tab macOS}}

**Install:** Text for macOS.

{{#endtab}}
{{#endtabs}}
```

In the browser the groups become tabs that work with the arrow keys, and a reader's choice applies to every group with the same labels, on every page. Without JavaScript, all tabs are shown one under another, each under its label. The linter rejects other labels, mixed sets and unbalanced markers.

## Diagrams

Use Mermaid in a ```` ```mermaid ```` fence, top to bottom (`flowchart TD`), with short node labels and no custom colors. Put one plain sentence that describes the diagram before it, for screen-reader users. Keep each row to at most two nodes: a wider diagram is scaled down on a phone until its text is too small, and the UI test for the diagram fails when text falls below 12px. Mermaid is bundled in `theme/` and draws in the colors of the current theme.

## Tables

A table wider than the page scrolls inside its frame, and the frame can be scrolled with the keyboard. Readers on phones should still not have to scroll: keep tables to three columns or fewer with short cells, and split a wide table into two.

## Browser tests and visual review

`make test-ui` builds the book and opens every page in a headless browser at nine widths (320 to 1920 pixels) in light and dark mode, served under the same path as on GitHub Pages. The list of pages comes from `docs/SUMMARY.md`, and a listed page that was not built is an error. It checks, among other things, that:

- the page never scrolls sideways and nothing sticks out of the text column,
- long code lines scroll inside their own block,
- there are no console errors or failed requests,
- axe-core finds no serious or critical accessibility problems (`tests/ui/axe_allowlist.json` is empty; an entry needs a written reason),
- every page has one `h1` in its content and no skipped heading levels,
- keyboard focus is visible on the controls readers use,
- the previous and next arrows follow `SUMMARY.md`, and the sidebar, search, theme menu and edit links work,
- tabs have the right roles, work with the keyboard, remember the choice and stay readable without JavaScript,
- answers stay hidden until opened, and the copy button copies the program in `examples/`,
- the Mermaid diagram draws in both themes and fits at 320 pixels,
- an unknown address shows the book's own 404 page, styled and with a working sidebar.

When a check fails, the test run saves a screenshot of the failing page to `artifacts/screenshots/failures/`, and CI uploads that folder. Optional settings: `UI_WORKERS` sets how many browsers run in parallel (`make test-ui UI_WORKERS=4`, default 2), and `BASE_URL` tests a published book instead of the local build, for example `BASE_URL=https://supernovified.github.io/learn-cpp-for-free/`.

Automated checks do not see everything, so look at the screenshots of your page (375 and 1280 pixels wide in both color schemes, plus 320 for pages with tabs, tables or diagrams) and check that:

1. callouts line up with the text, and the custom kinds look like the built-in ones;
2. the copy button never covers code, and file names line up with the block edges;
3. output blocks look different from code but line up with it;
4. tab labels sit on one line and nothing is clipped on a phone;
5. long sidebar titles wrap cleanly and the current page is clearly highlighted;
6. the arrows at the bottom of the page do not overlap the text on a phone;
7. tables have an aligned header row and padded cells;
8. there is no doubled or collapsed spacing, for example between a heading and a callout;
9. the dark theme has no white boxes and no dark-on-dark text;
10. the menu bar never collides at 320 to 414 pixels;
11. rendered keys do not disturb the line height;
12. no text is smaller than 12px, and inline code is legible in both themes.

## Content checklist

Before you open a pull request, check that:

1. the wording is original, with nothing copied or closely paraphrased;
2. every fact that can change was checked against a primary source today;
3. the lesson covers what it promises and does not teach later chapters in depth;
4. every complete program is an included, checked example;
5. each term is bolded once where it is defined, and used consistently afterwards;
6. callouts have the right kind and are not stacked or overused;
7. tabs use the exact label sets;
8. the length is reasonable and paragraphs have four sentences or fewer;
9. a summary is present, and further reading uses primary sources over https;
10. a beginner could follow every instruction without guessing.

## Commits and pull requests

Use Conventional Commits, `type(scope): description`, with one coherent change per commit. Common types are `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `build`, `ci` and `chore`. Examples: `docs(ch00): add lesson 0.14`, `fix(theme): keep icons aligned in callouts`.

Do not commit the virtual environment, `.tools/`, the `book/` folder, screenshots, caches or secrets. Open a pull request against `main` and fill in the checklist. Every check must be green before it can be merged.

Found a factual mistake? [Open an issue](https://github.com/SupernovifieD/learn-cpp-for-free/issues/new?template=content-error.md) or use the edit button in the top right corner of the page.
