# Changelog

All notable changes to The C++ Book are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.1.0]: https://github.com/SupernovifieD/learn-cpp-for-free/releases/tag/v0.1.0
