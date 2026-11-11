# Developer shortcuts. Run `make help` to list them.
# Written for GNU Make 3.81 (the version macOS ships), so no newer features.

# Virtual environment created by `make install` (ignored by git).
VENV ?= .venv

# Interpreter that runs mkdocs, pytest and the scripts. Point it at your own
# if you do not use the virtual environment, e.g. `make PY=python build`.
PY ?= $(VENV)/bin/python

# Interpreter used only to create the virtual environment.
BOOTSTRAP_PY ?= python3

.PHONY: help install serve build

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
