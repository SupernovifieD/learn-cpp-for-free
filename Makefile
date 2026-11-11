# Developer shortcuts. Run `make help` to list them.
# Written for GNU Make 3.81 (the version macOS ships), so no newer features.

# Virtual environment created by `make install` (ignored by git).
VENV ?= .venv

# Interpreter that runs mkdocs, pytest and the scripts. Point it at your own
# if you do not use the virtual environment, e.g. `make PY=python build`.
PY ?= $(VENV)/bin/python

# Interpreter used only to create the virtual environment.
BOOTSTRAP_PY ?= python3

# The pinned clang-format that `make format` and `make format-check` run. Point
# it at your own if you do not use the virtual environment.
CLANG_FORMAT ?= $(VENV)/bin/clang-format

# Extra options for scripts/check_examples.py. CI passes --require-all so that
# a missing compiler fails the build instead of only printing a warning.
EXAMPLES_ARGS ?=

# Options for scripts/lint_content.py. --final also rejects leftover <!-- STUB --> markers and
# requires lesson 0.11 to show the flags file, so no unfinished page can be published. CI uses
# this too. To draft a page with a stub marker locally, run `make lint LINT_ARGS=`.
LINT_ARGS ?= --final

# Every C++ example in the book.
CPP_FILES = $(shell find examples -name '*.cpp' | sort)

# Browser test workers. Each one runs its own Chromium (hundreds of MB), so the
# default is small enough for a laptop with 8 GB; raise it on a bigger machine,
# e.g. `make test-ui UI_WORKERS=4`.
UI_WORKERS ?= 2

.PHONY: help install serve build test-ui screenshots lint examples format format-check check

help: ## Show this list of targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sed -e 's/:.*## /\t/'

install: ## Create .venv and install all dependencies
	$(BOOTSTRAP_PY) -m venv $(VENV)
	$(PY) -m pip install -r requirements-dev.txt
	$(PY) -m playwright install chromium

serve: ## Preview the book at http://127.0.0.1:8000 with live reload
	$(PY) -m mkdocs serve

build: ## Build the site into site/, failing on any warning
	$(PY) -m mkdocs build --strict

test-ui: build ## Build, then run the browser tests (layout, accessibility, behavior)
	$(PY) -m pytest tests/ui -q --durations=5 -n $(UI_WORKERS) --dist loadscope

screenshots: build ## Build, then save screenshots of every page to artifacts/screenshots/
	$(PY) tests/ui/screenshots.py

lint: ## Check the structure and writing rules of docs/ (see scripts/lint_content.py)
	$(PY) scripts/lint_content.py $(LINT_ARGS)

examples: ## Compile, run and format-check every C++ example with GCC and Clang
	$(PY) scripts/check_examples.py $(EXAMPLES_ARGS)

format: ## Reformat every C++ example in place
	$(CLANG_FORMAT) -i $(CPP_FILES)

format-check: ## Fail if any C++ example is not formatted (changes nothing)
	$(CLANG_FORMAT) --dry-run --Werror $(CPP_FILES)

check: lint examples format-check build test-ui ## Everything CI checks: lint, examples, format, build, browser tests
