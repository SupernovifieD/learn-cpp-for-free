# The C++ Book

A free, open-source book for learning modern C++ from first principles. It is built with [mdBook](https://rust-lang.github.io/mdBook/), the tool behind [The Rust Programming Language](https://doc.rust-lang.org/book/), and reads like it: a table of contents on the left, previous and next arrows, full-text search, and light and dark themes.

**Read it online: <https://supernovified.github.io/learn-cpp-for-free/>**

This is a pilot. It contains the introduction, the home page, a page that explains the conventions used in the book, and **Chapter 0 (Introduction / Getting Started)** with 13 lessons. Every complete program in the book is compiled with GCC and Clang, using C++20 and strict warnings, and its output is checked automatically.

## Quick start

You need Python 3.11 or newer, `make`, Git and a C++ compiler. Then:

```bash
git clone https://github.com/SupernovifieD/learn-cpp-for-free.git
cd learn-cpp-for-free
make install   # downloads the pinned mdBook tools and sets up the test environment
make serve     # builds the book and reloads it when you save a file
```

Open <http://127.0.0.1:3000> to read the book while you edit it. `make build` writes the finished site to `book/`. [CONTRIBUTING.md](CONTRIBUTING.md) has the full setup (including Windows), the daily workflow and the rules for lessons.

## How the repository is organized

| Path | What it holds |
| --- | --- |
| `docs/` | Everything the book publishes: the pages, and `SUMMARY.md`, the table of contents |
| `examples/` | Every complete C++ program in the book, with its expected output |
| `book.toml` | The mdBook configuration |
| `theme/` | The few additions to mdBook's own look: one stylesheet, one script, the favicon, Mermaid, and a highlight.js bundle with PowerShell |
| `scripts/` | The example checker, the content linter, the mdBook preprocessor and the tool installer |
| `tests/ui/` | Browser tests for layout, accessibility and behavior |
| `templates/` | Copy-me starting points for a new lesson and a new chapter |
| `.github/` | The CI workflow, Dependabot and the pull request and issue templates |

## How it is checked and published

`make check` runs everything that CI runs: it lints the content, builds and runs the C++ examples with GCC and Clang, checks their formatting, builds the book, and runs the browser tests against it.

A GitHub Actions workflow repeats these checks for every push and pull request. When a change lands on `main` and every check passes, the same workflow uploads `book/` and publishes it to GitHub Pages, and then checks that the published address serves the new book.

## Technology

The book is built with mdBook 0.5.4 and mdbook-mermaid 0.17.1 (pinned in `scripts/install_tools.py`). A small Python script, `scripts/mdbook_cppbook.py`, adds file-name labels, a few callout kinds and tabs. Python is also used for the checks and the browser tests, but not by mdBook itself.

## License

The project is released under the [MIT License](LICENSE).

## Acknowledgements

The order of chapters and lessons follows the outline of [LearnCpp.com](https://www.learncpp.com/). Every explanation, example and exercise in this book is original.
