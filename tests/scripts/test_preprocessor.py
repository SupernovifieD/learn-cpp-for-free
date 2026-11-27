"""Tests for charts and data tables generated from checked program output."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from mdbook_cppbook import SyntaxProblem, convert  # noqa: E402


@pytest.fixture
def checked_output(tmp_path):
    page = tmp_path / "docs" / "ch06" / "page.md"
    page.parent.mkdir(parents=True)
    examples = tmp_path / "examples" / "ch06"
    examples.mkdir(parents=True)

    def write(name: str, data: str, suffix: str = ".out") -> tuple[Path, str]:
        (examples / f"{name}.cpp").write_text("int main() {}\n")
        output = examples / f"{name}{suffix}"
        output.write_text(data)
        if suffix == ".example":
            (examples / f"{name}.match").write_text(".*\n" * len(data.splitlines()))
        relative = f"../../examples/ch06/{name}{suffix}"
        return page, relative

    return tmp_path, write


def render(tmp_path: Path, page: Path, directive: str) -> str:
    return convert(directive, page, tmp_path)


def test_bar_chart_has_accessibility_text_axes_zero_baseline_and_data_table(checked_output):
    root, write = checked_output
    page, data = write("values", "first 2\nsecond 5\n")
    output = render(root, page, f'{{{{#chart bar {data} x="Pass" y="Value" caption="Values by pass"}}}}')

    assert "```mermaid\nxychart-beta" in output
    assert "accTitle: Values by pass" in output
    assert 'x-axis "Pass" ["first", "second"]' in output
    assert 'y-axis "Value" 0 --> 5' in output
    assert "bar [2, 5]" in output
    assert "<summary>Data for this chart</summary>" in output
    assert "| second | 5 |" in output


def test_line_chart_accepts_negative_values_and_computes_its_range(checked_output):
    root, write = checked_output
    page, data = write("remainders", "minus -2\nzero 0\nplus 2\n")
    output = render(root, page, f'{{{{#chart line {data} x="Input" y="Remainder" caption="Remainders"}}}}')

    assert 'y-axis "Remainder" -2 --> 2' in output
    assert "line [-2, 0, 2]" in output


def test_example_output_adds_one_example_run_to_the_caption(checked_output):
    root, write = checked_output
    page, data = write("roll", "face 4\n", suffix=".example")
    output = render(root, page, f'{{{{#chart bar {data} x="Kind" y="Roll" caption="A die roll"}}}}')

    assert "accTitle: A die roll (one example run)" in output
    assert 'title "A die roll (one example run)"' in output


def test_table_splits_rows_to_match_one_to_three_headers(checked_output):
    root, write = checked_output
    page, data = write("trace", "one 2 yes\ntwo 4 no\n")
    output = render(root, page, f'{{{{#table {data} header="Pass | Value | Kept"}}}}')

    assert output == "| Pass | Value | Kept |\n| --- | --- | --- |\n| one | 2 | yes |\n| two | 4 | no |"


def test_skip_ignores_leading_lines(checked_output):
    root, write = checked_output
    page, data = write("headed", "label value\none 1\n")
    output = render(root, page, f'{{{{#table {data} header="Name | Value" skip=1}}}}')

    assert "label" not in output
    assert "| one | 1 |" in output


@pytest.mark.parametrize(
    ("data", "directive", "message"),
    [
        ("one\n", 'table DATA header="A | B"', "has 1 fields"),
        ("one 1 extra\n", 'chart line DATA x="A" y="B" caption="C"', "exactly a label and a number"),
        ("one nope\n", 'chart line DATA x="A" y="B" caption="C"', "non-number"),
        ("one -1\n", 'chart bar DATA x="A" y="B" caption="C"', "negative value"),
    ],
)
def test_bad_data_stops_the_build(checked_output, data, directive, message):
    root, write = checked_output
    page, data_file = write("bad", data)
    with pytest.raises(SyntaxProblem, match=message):
        render(root, page, "{{#" + directive.replace("DATA", data_file) + "}}")


@pytest.mark.parametrize(
    ("rows", "directive", "maximum"),
    [
        (13, 'chart line DATA x="A" y="B" caption="C"', 12),
        (17, 'table DATA header="A | B"', 16),
    ],
)
def test_row_limits_stop_the_build(checked_output, rows, directive, maximum):
    root, write = checked_output
    page, data_file = write("long", "".join(f"row{row} {row}\n" for row in range(rows)))
    with pytest.raises(SyntaxProblem, match=f"at most {maximum}"):
        render(root, page, "{{#" + directive.replace("DATA", data_file) + "}}")


def test_more_than_three_table_columns_stops_the_build(checked_output):
    root, write = checked_output
    page, data = write("wide", "a b c d\n")
    with pytest.raises(SyntaxProblem, match="between 1 and 3"):
        render(root, page, f'{{{{#table {data} header="A | B | C | D"}}}}')


def test_missing_file_stops_the_build(checked_output):
    root, write = checked_output
    page, _ = write("present", "one 1\n")
    with pytest.raises(SyntaxProblem, match="does not exist"):
        render(root, page, '{{#table missing.out header="A | B"}}')


def test_file_that_is_not_a_checked_companion_stops_the_build(checked_output):
    root, write = checked_output
    page, _ = write("values", "one 1\n")
    plain = page.parent / "values.txt"
    plain.write_text("one 1\n")
    with pytest.raises(SyntaxProblem, match="not a checked output companion"):
        render(root, page, '{{#table values.txt header="A | B"}}')


def test_output_without_a_program_stops_the_build(checked_output):
    root, write = checked_output
    page, data = write("orphan", "one 1\n")
    (root / "examples" / "ch06" / "orphan.cpp").unlink()
    with pytest.raises(SyntaxProblem, match="has no checked program"):
        render(root, page, f'{{{{#table {data} header="A | B"}}}}')


@pytest.mark.parametrize(
    ("directive", "message"),
    [
        ('{{#chart pie data.out x="A" y="B" caption="C"}}', "use bar or line"),
        ('{{#chart bar data.out x="A" y="B"}}', "missing: caption"),
        ('{{#table data.out header="A" skip=-1}}', "non-negative whole number"),
        ('{{#table data.out header="A" mystery=yes}}', "unknown 'mystery' option"),
        ('  {{#table data.out header="A"}}', "must start at the beginning"),
        ('before {{#table data.out header="A"}}', "occupy one complete line"),
    ],
)
def test_bad_directive_syntax_stops_the_build(checked_output, directive, message):
    root, write = checked_output
    page, _ = write("data", "one\n")
    with pytest.raises(SyntaxProblem, match=message):
        render(root, page, directive)


def test_visual_directive_inside_a_code_fence_is_left_alone(checked_output):
    root, write = checked_output
    page, _ = write("data", "one 1\n")
    source = '```text\n{{#table missing.out header="A | B"}}\n```'

    assert render(root, page, source) == source
