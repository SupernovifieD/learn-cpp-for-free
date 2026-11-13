# Developer shortcuts. Run `make help` to list them.
# Written for GNU Make 3.81 (the version macOS ships), so no newer features.

# Virtual environment created by `make install` (ignored by git).
VENV ?= .venv

# Interpreter that runs pytest and the scripts. Point it at your own if you do
# not use the virtual environment, e.g. `make PY=python lint`.
PY ?= $(VENV)/bin/python

# Where scripts/install_tools.py puts the pinned mdbook and mdbook-mermaid
# (ignored by git). It goes first on PATH, so mdBook finds its preprocessors.
TOOLS_BIN = $(CURDIR)/.tools/bin
MDBOOK = PATH="$(TOOLS_BIN):$$PATH" mdbook

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

install: ## Download the pinned mdBook tools, create .venv and install the test dependencies
	$(BOOTSTRAP_PY) scripts/install_tools.py
	$(BOOTSTRAP_PY) -m venv $(VENV)
	$(PY) -m pip install -r requirements-dev.txt
	$(PY) -m playwright install chromium

serve: ## Preview the book at http://127.0.0.1:3000 with live reload
	$(MDBOOK) serve

# mdBook only logs a problem such as an include of a missing file and still exits with success, so
# the build also fails when the log has a WARN or ERROR line. (The note that mdbook-mermaid was
# built against an older mdBook 0.5 release is neither; it is expected and harmless.)
build: ## Build the book into book/, failing on any warning or error
	@log=$$($(MDBOOK) build 2>&1); status=$$?; printf '%s\n' "$$log"; \
	if [ $$status -ne 0 ] || printf '%s\n' "$$log" | grep -Eq '^[[:space:]]*(WARN|ERROR)[[:space:]]'; then \
		echo "The build reported a problem (see above)." >&2; exit 1; \
	fi

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

check: lint examples format-check test-ui ## Everything CI checks: lint, examples, format, build, browser tests
