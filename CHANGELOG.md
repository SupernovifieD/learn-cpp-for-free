# Changelog

All notable changes to The C++ Book are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Chapter 1, "C++ Basics": 11 lessons, from statements and comments to
  variables, input and output, operators, expressions and a first program,
  and a summary and quiz page.
- Chapter 2, "C++ Basics: Functions and Files": 13 lessons on functions,
  scope, several source files, namespaces, the preprocessor, header files and
  header guards, and a summary and quiz page.
- Chapter 3, "Debugging C++ Programs": 10 lessons on the kinds of errors, the
  debugging process and strategy, printing to the error stream, switching debug
  output on and off, using a debugger (stepping, breakpoints, watching variables
  and the call stack, with Visual Studio, VS Code, GDB and LLDB), and finding
  problems early with warnings, static analysis, tests and sanitizers, and a
  summary and quiz page.
- Chapter 4, "Fundamental Data Types": 12 lessons on bits and types, sizes,
  signed and unsigned integers, fixed-width integers, scientific notation,
  floating point numbers, Booleans, `if` statements, characters and
  `static_cast`, and a summary and quiz page.
- Chapter 5, "Constants and Strings": 9 lessons on `const`, literals, numeral
  systems, the as-if rule, constant expressions, `constexpr`, `std::string` and
  `std::string_view`, and a summary and quiz page.
- Example programs that write to the error stream. `X.err` holds exactly what a
  program writes to standard error, and `X.out` or `X.session` shows the console
  view, with both streams in the order in which the program wrote them.
- Example programs with undefined behavior (`X.ub.cpp`). The checker builds them
  without `-Werror` and with the sanitizers, and requires a non-zero exit status
  and a sanitizer report. A lesson shows them without output.
- Checked GDB walkthroughs. `X.gdb` holds the commands and `X.gdb-expect` the
  texts that GDB must print, in order. CI installs gdb if it is missing.
- `make test-ui UI_ONLY=<text>` runs only the browser tests whose id contains
  the text, for drafting. `make check` refuses it, and CI never sets it.
- A browser test that fails a Mermaid diagram that renders as "Unsupported
  markdown", and search tests for "breakpoint", "scientific notation" and
  "string_view".
- Example programs of several files. A program in `examples/` is a file or a
  folder with `.cpp` and `.h` files that are built together, and headers are
  checked for length and formatting like the sources.
- Console sessions for programs that read input. `X.in` holds what the reader
  types, and `X.session` holds what the reader sees, which the checker proves
  against the output of the program.
- Every running example is also built and run with AddressSanitizer and UBSan.
- Tests for the example checker itself, with example trees that it must accept
  or reject (`make test-scripts`), run in `make check` and in CI.
- Browser tests for every page with answers, measured again with all of them
  opened, and for every page with a diagram, and a search test for "header
  guard".
- A template for summary and quiz pages, and contributor rules for projects,
  sessions, quiz pages, naming and the order in which topics are taught.

### Changed

- The browser test that checks that a page never scrolls sideways now also
  checks the text area, which mdBook lets scroll on its own and which used to
  hide an element that was too wide.
- `tests/ui/screenshots.py` can open all answers, choose pages and choose
  widths.
- Forward references in Chapter 0 link to the lessons that explain them.
- Forward references in Chapters 0 to 2 link to the lessons of Chapters 3 to 5 that explain them.

### Fixed

- The example checker looked for `X.out` instead of `X.fail.out` when it
  checked a failing program, so a stray `X.fail.out` file went unnoticed.

## [0.2.0] - 2026-11-13

### Changed

- Moved the book from MkDocs to [mdBook](https://rust-lang.github.io/mdBook/),
  pinned at 0.5.4, so that it reads like The Rust Programming Language. The
  table of contents is now `docs/SUMMARY.md`, includes use `{{#include}}`,
  callouts are block quotes such as `> [!NOTE]`, keys use `<kbd>`, and questions
  use `<details>`. The lessons' wording and the C++ examples are unchanged.
- Pages are now published as `.html` files, such as `conventions.html`. The old
  directory-style addresses, such as `/conventions/`, are not redirected and now
  show the book's 404 page. The home page and `ch00-getting-started/` keep their
  addresses.
- Pages no longer have front matter, so every page uses the book's description.
- The book has two themes, light and Navy, instead of the old blue palette.
- Rewrote the content linter, the browser tests, the Makefile, the CI workflow,
  the templates and the contributor guide for mdBook. `make install` now
  downloads checksum-verified mdBook tools into `.tools/`.

### Added

- A small preprocessor (`scripts/mdbook_cppbook.py`) for file-name labels on
  code blocks, the danger, best-practice, key-insight and advanced callouts, and
  platform tabs with keyboard support that remember the reader's choice.
- A check after each deployment that the published book is the mdBook build.

### Removed

- MkDocs, Material for MkDocs, pymdown-extensions, PyYAML, the old stylesheet
  and the old logo.

### Fixed

- A browser test of keyboard focus looked for the copy button before mdBook had
  made it visible, which made it fail on slow machines.

## [0.1.0] - 2026-11-12

### Added

- Published the first complete pilot of The C++ Book, including the home page,
  reading conventions, the Chapter 0 overview, and 13 original lessons that
  take a new learner from programming fundamentals through selecting and
  detecting a C++ language standard.
- Added six C++ examples covering a first program, linker failures, missing
  includes, compiler extensions, warnings as errors, and language-standard
  detection. Examples are compiled with GCC and Clang under strict C++20
  settings, and expected successes, failures, formatting, and output are
  checked automatically.
- Created a responsive MkDocs Material reading experience with explicit
  navigation, full-text search, light and dark themes, accessible callouts,
  code-copy controls, diagrams, previous and next links, and original branding.
- Added automated content linting, strict site builds, and browser coverage for
  layout, accessibility, navigation, search, diagrams, color schemes, and
  behavior across phone, tablet, and desktop widths.
- Added GitHub Actions checks for every push and pull request, automatic GitHub
  Pages deployment from `main`, Dependabot updates, and diagnostic screenshots
  for browser-test failures.
- Added contributor setup and writing guidance, lesson and chapter templates,
  pull request and content-error templates, and local `make` targets that match
  the continuous-integration checks.
- Released the project under the MIT License.

### Fixed

- Grouped parallel browser tests by viewport and color scheme so each page is
  loaded once per group, restoring the intended page reuse and cutting
  unnecessary repeated work.

[Unreleased]: https://github.com/SupernovifieD/learn-cpp-for-free/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/SupernovifieD/learn-cpp-for-free/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/SupernovifieD/learn-cpp-for-free/releases/tag/v0.1.0
