"""Tests for the part of scripts/lint_content.py that decides whether every example file is used."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import lint_content  # noqa: E402


@pytest.fixture
def examples(tmp_path, monkeypatch):
    """A temporary stand-in for the repository, with lint_content pointed at it."""
    monkeypatch.setattr(lint_content, "REPO", tmp_path)
    monkeypatch.setattr(lint_content, "EXAMPLES", tmp_path / "examples")

    def write(files: list[str]) -> None:
        for name in files:
            path = tmp_path / "examples" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("")

    return write


def problems_for(used: set[str]) -> list[str]:
    return [str(problem) for problem in lint_content.lint_examples_used({"ch01/page.md": used}, final=False)]


def test_every_file_of_a_project_must_be_included_by_a_page(examples):
    examples(["ch01/02-add/main.cpp", "ch01/02-add/add.cpp", "ch01/02-add/add.h", "ch01/02-add.out"])
    used = {"examples/ch01/02-add/main.cpp", "examples/ch01/02-add/add.cpp", "examples/ch01/02-add.out"}
    problems = problems_for(used)
    assert len(problems) == 1 and "add.h" in problems[0] and "is not used by any page" in problems[0]


def test_a_fully_included_project_has_no_problems(examples):
    files = ["ch01/02-add/main.cpp", "ch01/02-add/add.h", "ch01/02-add.out"]
    examples(files)
    assert problems_for({f"examples/{name}" for name in files}) == []


def test_an_input_file_may_belong_to_a_project_folder_next_to_it(examples):
    examples(["ch01/02-add/main.cpp", "ch01/02-add.in"])
    assert problems_for({"examples/ch01/02-add/main.cpp"}) == []


def test_an_input_file_may_belong_to_a_single_file_program(examples):
    examples(["ch01/01-read.cpp", "ch01/01-read.in"])
    assert problems_for({"examples/ch01/01-read.cpp"}) == []


def test_an_input_file_without_a_program_is_reported(examples):
    examples(["ch01/01-a.cpp", "ch01/09-orphan.in"])
    problems = problems_for({"examples/ch01/01-a.cpp"})
    assert len(problems) == 1 and "09-orphan.in" in problems[0] and "no program" in problems[0]


def test_a_session_must_be_included_by_a_page(examples):
    examples(["ch01/01-read.cpp", "ch01/01-read.in", "ch01/01-read.session"])
    problems = problems_for({"examples/ch01/01-read.cpp"})
    assert len(problems) == 1 and "01-read.session" in problems[0] and "is not used by any page" in problems[0]
    assert problems_for({"examples/ch01/01-read.cpp", "examples/ch01/01-read.session"}) == []


def test_a_standard_error_file_belongs_to_its_program_and_needs_no_include(examples):
    examples(["ch01/01-trace.cpp", "ch01/01-trace.out", "ch01/01-trace.err", "ch01/02-proj/main.cpp", "ch01/02-proj.out", "ch01/02-proj.err"])
    used = {"examples/ch01/01-trace.cpp", "examples/ch01/01-trace.out", "examples/ch01/02-proj/main.cpp", "examples/ch01/02-proj.out"}
    assert problems_for(used) == []


def test_a_standard_error_file_without_a_program_is_reported(examples):
    examples(["ch01/01-a.cpp", "ch01/09-orphan.err"])
    problems = problems_for({"examples/ch01/01-a.cpp"})
    assert len(problems) == 1 and "09-orphan.err" in problems[0] and "standard error file has no program next to it" in problems[0]


def test_an_exit_status_file_belongs_to_its_program_and_needs_no_include(examples):
    examples(["ch01/01-stop.cpp", "ch01/01-stop.out", "ch01/01-stop.status"])
    used = {"examples/ch01/01-stop.cpp", "examples/ch01/01-stop.out"}
    assert problems_for(used) == []


def test_an_exit_status_file_without_a_program_is_reported(examples):
    examples(["ch01/01-a.cpp", "ch01/09-orphan.status"])
    problems = problems_for({"examples/ch01/01-a.cpp"})
    assert len(problems) == 1
    assert "09-orphan.status" in problems[0] and "exit status file has no program next to it" in problems[0]


def test_a_match_file_belongs_to_its_program_but_the_example_must_be_included(examples):
    examples(["ch01/01-die.cpp", "ch01/01-die.match", "ch01/01-die.example"])
    source = "examples/ch01/01-die.cpp"
    example = "examples/ch01/01-die.example"
    problems = problems_for({source})
    assert len(problems) == 1 and "01-die.example" in problems[0] and "is not used by any page" in problems[0]
    assert problems_for({source, example}) == []


def test_a_page_cannot_include_a_match_file(examples):
    examples(["ch01/01-die.cpp", "ch01/01-die.match", "ch01/01-die.example"])
    used = {"examples/ch01/01-die.cpp", "examples/ch01/01-die.match", "examples/ch01/01-die.example"}
    problems = problems_for(used)
    assert len(problems) == 1
    assert "remove the .match include and include its .example file instead" in problems[0]


def test_an_undefined_behavior_program_must_be_included_but_its_input_file_need_not_be(examples):
    examples(["ch04/04-overflow.ub.cpp", "ch04/04-overflow.ub.in", "ch04/05-divide.ub/main.cpp", "ch04/05-divide.ub.in"])
    assert problems_for({"examples/ch04/04-overflow.ub.cpp", "examples/ch04/05-divide.ub/main.cpp"}) == []
    problems = problems_for({"examples/ch04/05-divide.ub/main.cpp"})
    assert len(problems) == 1 and "04-overflow.ub.cpp" in problems[0] and "is not used by any page" in problems[0]


def test_an_input_file_of_an_undefined_behavior_program_without_a_program_is_reported(examples):
    examples(["ch04/04-overflow.ub.cpp", "ch04/09-gone.ub.in"])
    problems = problems_for({"examples/ch04/04-overflow.ub.cpp"})
    assert len(problems) == 1 and "09-gone.ub.in" in problems[0] and "no program next to it" in problems[0]


def test_a_walkthrough_must_be_included_but_its_expectations_need_not_be(examples):
    examples(["ch03/06-steps.cpp", "ch03/06-steps.out", "ch03/06-steps.gdb", "ch03/06-steps.gdb-expect"])
    used = {"examples/ch03/06-steps.cpp", "examples/ch03/06-steps.out", "examples/ch03/06-steps.gdb"}
    assert problems_for(used) == []
    problems = problems_for(used - {"examples/ch03/06-steps.gdb"})
    assert len(problems) == 1 and "06-steps.gdb:" in problems[0] and "is not used by any page" in problems[0]


def test_walkthrough_expectations_without_a_walkthrough_are_reported(examples):
    examples(["ch03/06-steps.cpp", "ch03/09-gone.gdb-expect"])
    problems = problems_for({"examples/ch03/06-steps.cpp"})
    assert len(problems) == 1 and "09-gone.gdb-expect" in problems[0] and "has no 09-gone.gdb next to it" in problems[0]


def test_files_the_operating_system_adds_are_not_examples(examples):
    examples(["ch01/01-a.cpp", "ch01/.DS_Store"])
    assert problems_for({"examples/ch01/01-a.cpp"}) == []


# ------------------------------------------------ checked-data visuals --


def visual_page(tmp_path, monkeypatch, body: str, files: dict[str, str]):
    monkeypatch.setattr(lint_content, "REPO", tmp_path)
    monkeypatch.setattr(lint_content, "DOCS", tmp_path / "docs")
    monkeypatch.setattr(lint_content, "EXAMPLES", tmp_path / "examples")
    page = tmp_path / "docs" / "ch06" / "page.md"
    page.parent.mkdir(parents=True)
    page.write_text("# 6.1 Test\n\n" + body + "\n")
    for name, content in files.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return lint_content.lint_page(page, "6.1 Test", "Book", final=False)


def test_chart_data_counts_as_used_and_its_program_is_on_the_same_page(tmp_path, monkeypatch):
    body = """This chart shows the value for each pass.

{{#chart bar ../../examples/ch06/values.out x="Pass" y="Value" caption="Values"}}

This is the program behind the chart.

```cpp title="values.cpp"
{{#include ../../examples/ch06/values.cpp}}
```"""
    page = visual_page(
        tmp_path,
        monkeypatch,
        body,
        {"examples/ch06/values.cpp": "int main() {}\n", "examples/ch06/values.out": "one 1\n"},
    )

    assert page.problems == []
    assert "examples/ch06/values.out" in page.included
    assert "examples/ch06/values.cpp" in page.included


def test_data_visual_requires_its_program_on_the_same_page(tmp_path, monkeypatch):
    page = visual_page(
        tmp_path,
        monkeypatch,
        'This table shows the value for each pass.\n\n{{#table ../../examples/ch06/values.out header="Pass | Value"}}',
        {"examples/ch06/values.cpp": "int main() {}\n", "examples/ch06/values.out": "one 1\n"},
    )

    messages = [problem.message for problem in page.problems]
    assert any("program behind this table must be included on the same page" in message for message in messages)


def test_data_visual_requires_every_file_of_a_project_on_the_same_page(tmp_path, monkeypatch):
    body = """This chart shows the trace made by the project.

{{#chart line ../../examples/ch06/trace.out x="Pass" y="Value" caption="Trace"}}

This is the project's entry point.

```cpp title="main.cpp"
{{#include ../../examples/ch06/trace/main.cpp}}
```"""
    page = visual_page(
        tmp_path,
        monkeypatch,
        body,
        {
            "examples/ch06/trace/main.cpp": "int main() {}\n",
            "examples/ch06/trace/helper.cpp": "void helper() {}\n",
            "examples/ch06/trace.out": "one 1\n",
        },
    )

    messages = [problem.message for problem in page.problems]
    assert any("helper.cpp" in message and "same page" in message for message in messages)


def test_malformed_data_visual_has_an_actionable_lint_error(tmp_path, monkeypatch):
    page = visual_page(tmp_path, monkeypatch, 'This chart shows each pass.\n\n{{#chart bar values.out x="Pass"}}', {})

    messages = [problem.message for problem in page.problems]
    assert any("missing: caption, y" in message for message in messages)


# ---------------------------------------------------- concept-first visuals --


def visual_rule_messages(tmp_path, monkeypatch, body: str, name: str = "01-lesson.md") -> list[str]:
    monkeypatch.setattr(lint_content, "REPO", tmp_path)
    monkeypatch.setattr(lint_content, "DOCS", tmp_path / "docs")
    monkeypatch.setattr(lint_content, "EXAMPLES", tmp_path / "examples")
    page = tmp_path / "docs" / "ch06-operators" / name
    page.parent.mkdir(parents=True)
    label = "6.1 Test" if name != "index.md" else "6. Operators"
    page.write_text(f"# {label}\n\n{body}\n")
    result = lint_content.lint_page(page, label, "Book", final=False)
    return [problem.message for problem in result.problems]


def test_chapter_six_lesson_without_a_visual_is_rejected(tmp_path, monkeypatch):
    messages = visual_rule_messages(tmp_path, monkeypatch, "The lesson has prose but no picture.")

    assert any("need at least one Mermaid diagram" in message for message in messages)


def test_chapter_six_index_without_a_visual_is_rejected(tmp_path, monkeypatch):
    messages = visual_rule_messages(tmp_path, monkeypatch, "The chapter has prose but no concept map.", name="index.md")

    assert any("need at least one Mermaid diagram" in message for message in messages)


def test_code_before_the_first_lesson_visual_is_rejected(tmp_path, monkeypatch):
    body = """This fragment comes too early.

```cpp
int value{2};
```

This diagram shows where the value goes.

```mermaid
flowchart TD
    value[Value] --> output[Output]
```"""
    messages = visual_rule_messages(tmp_path, monkeypatch, body)

    assert any("first visual" in message and "before" in message for message in messages)


def test_heading_immediately_before_a_visual_is_rejected(tmp_path, monkeypatch):
    body = """## The path

```mermaid
flowchart TD
    start[Start] --> finish[Finish]
```"""
    messages = visual_rule_messages(tmp_path, monkeypatch, body)

    assert any("plain prose sentence immediately before" in message for message in messages)


def test_mermaid_init_directive_is_rejected(tmp_path, monkeypatch):
    body = """This diagram shows one step.

```mermaid
%%{init: {"flowchart": {"padding": 6}}}%%
flowchart TD
    start[Start]
```"""
    messages = visual_rule_messages(tmp_path, monkeypatch, body)

    assert any("configuration belongs in theme/mermaid-init.js" in message for message in messages)


@pytest.mark.parametrize("entity", ["#43;", "&#42;"])
def test_html_entity_code_in_mermaid_is_rejected(tmp_path, monkeypatch, entity):
    body = f"""This diagram shows an operator.

```mermaid
flowchart TD
    operator[{entity}]
```"""
    messages = visual_rule_messages(tmp_path, monkeypatch, body)

    assert any("HTML entity code" in message and entity in message for message in messages)


# ------------------------------------------------------------- templates --

TEMPLATES = Path(__file__).resolve().parents[2] / "templates"


@pytest.mark.parametrize("template", ["lesson.md", "chapter-index.md", "summary-and-quiz.md"])
def test_a_page_that_is_still_a_template_is_rejected(tmp_path, monkeypatch, template):
    monkeypatch.setattr(lint_content, "REPO", tmp_path)
    monkeypatch.setattr(lint_content, "DOCS", tmp_path / "docs")
    page = tmp_path / "docs" / "ch01" / "page.md"
    page.parent.mkdir(parents=True)
    page.write_text((TEMPLATES / template).read_text())
    problems = lint_content.lint_page(page, "label", "Book", final=False).problems
    assert any("template is still here" in problem.message for problem in problems), [str(p) for p in problems]


def test_every_placeholder_phrase_of_the_quiz_template_is_known_to_the_linter():
    text = (TEMPLATES / "summary-and-quiz.md").read_text()
    phrases = [phrase for phrase in lint_content.TEMPLATE_LEFTOVERS if phrase in text]
    for expected in ("# N.x Chapter N summary and quiz", "what this page recaps", "Restate the key terms of the lesson", "Write the first question here", "Explain the solution here"):
        assert expected in phrases, f"'{expected}' is not in TEMPLATE_LEFTOVERS, or no longer in the quiz template."


@pytest.mark.parametrize(
    ("template", "name"),
    [("lesson.md", "01-lesson.md"), ("chapter-index.md", "index.md")],
)
def test_chapter_six_templates_satisfy_the_visual_structure_rules(tmp_path, monkeypatch, template, name):
    monkeypatch.setattr(lint_content, "REPO", tmp_path)
    monkeypatch.setattr(lint_content, "DOCS", tmp_path / "docs")
    page = tmp_path / "docs" / "ch06-example" / name
    page.parent.mkdir(parents=True)
    page.write_text((TEMPLATES / template).read_text())
    problems = lint_content.lint_page(page, None, "Book", final=False).problems
    visual_rule_phrases = (
        "need at least one Mermaid diagram",
        "first visual",
        "plain prose sentence immediately before",
        "configuration belongs in theme/mermaid-init.js",
        "HTML entity code",
    )

    assert not [problem for problem in problems if any(phrase in problem.message for phrase in visual_rule_phrases)]


@pytest.mark.parametrize("text", ["This is simply wrong.", "It just works.", "Obviously so.", "an easy fix", "TODO later"])
def test_the_words_that_the_style_guide_bans_are_forbidden(text):
    assert lint_content.FORBIDDEN_WORDS.search(text), text


@pytest.mark.parametrize("text", ["a just-in-time compiler", "adjust the width", "justify the text", "a simple fix", "the easiest way"])
def test_words_that_only_contain_a_banned_word_are_allowed(text):
    assert not lint_content.FORBIDDEN_WORDS.search(text), text
