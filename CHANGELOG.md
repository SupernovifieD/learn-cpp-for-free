# Changelog

All notable changes to The C++ Book are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
