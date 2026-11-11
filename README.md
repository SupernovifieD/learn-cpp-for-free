# The C++ Book

A free, open-source book for learning modern C++ from first principles. It aims to be calm and readable, in the spirit of [The Rust Programming Language](https://doc.rust-lang.org/book/): a numbered table of contents on the left, previous and next links, full-text search, and light and dark themes.

**Read it online: <https://supernovified.github.io/learn-cpp-for-free/>**

This is a pilot. It contains the introduction, the home page, a page that explains the conventions used in the book, and **Chapter 0 (Introduction / Getting Started)** with 13 lessons. Every complete program in the book is compiled with GCC and Clang, using C++20 and strict warnings, and its output is checked automatically.

## Quick start

You need Python 3.11 or newer, `make` and a C++ compiler. Then:

```bash
git clone https://github.com/SupernovifieD/learn-cpp-for-free.git
cd learn-cpp-for-free
make install
make serve
```

Open <http://127.0.0.1:8000> to read the book while you edit it. [CONTRIBUTING.md](CONTRIBUTING.md) has the full setup (including Windows), the daily workflow and the rules for lessons.

## How the repository is organized

| Path | What it holds |
| --- | --- |
| `docs/` | Everything the site publishes: the pages, the logo and the single stylesheet |
| `examples/` | Every complete C++ program in the book, with its expected output |
| `scripts/` | The example checker and the content linter |
| `tests/ui/` | Browser tests for layout, accessibility and behavior |
| `templates/` | Copy-me starting points for a new lesson and a new chapter |
| `mkdocs.yml` | The site configuration and the table of contents |
| `.github/` | The CI workflow, Dependabot and the pull request and issue templates |

## How it is checked and published

`make check` runs everything that CI runs: it lints the content, builds and runs the C++ examples with GCC and Clang, checks their formatting, builds the site with warnings as errors, and runs the browser tests.

A GitHub Actions workflow repeats these checks for every push and pull request. When a change lands on `main` and every check passes, the same workflow publishes the site to GitHub Pages.

## Technology

The site is built with [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. Material is in maintenance, and its team has announced that its end of life is May 5, 2027 (see the [official notice](https://zensical.org/upcoming-changes/)), so the book uses only built-in features and no custom theme code. That keeps it easy to move to [Zensical](https://zensical.org/), which can read `mkdocs.yml` directly.

## License

The project is released under the [MIT License](LICENSE).

## Acknowledgements

The order of chapters and lessons follows the outline of [LearnCpp.com](https://www.learncpp.com/). Every explanation, example and exercise in this book is original.
