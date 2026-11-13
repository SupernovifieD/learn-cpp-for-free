<!--
  HOW TO USE THIS TEMPLATE
  1. Copy this file to docs/chNN-slug/NN-slug.md (two-digit numbers, kebab-case slug).
  2. Replace every placeholder, then delete every comment like this one.
  3. Add the page to docs/SUMMARY.md with the same label as the heading below,
     and add it to the list in the chapter's index.md.
  4. Read CONTRIBUTING.md for the full rules, then run: make check
-->

<!--
  HEADING: exactly one level-1 heading, written as "<chapter>.<lesson> <Title>".
  It must be identical to the page's label in docs/SUMMARY.md.
-->

# 0.14 Title of the lesson

<!--
  OPENING PARAGRAPH: 2 to 4 sentences. Say what the lesson covers and why it
  matters to the reader.
-->

Say in two to four sentences what this lesson covers and why it matters.

<!--
  SECTIONS: level-2 headings in sentence case. Use a level-3 heading only when
  you need one, and never skip a level. Keep paragraphs to four sentences or fewer.
  Write to "you", in American English. Bold a term where you define it.
-->

## First section

Explain one idea per section. Put identifiers, file names and commands in backticks.

<!--
  PROGRAMS: never paste a complete program here. Put it in examples/chNN/NN-slug.cpp
  with its output in NN-slug.out, then include both files with the include syntax
  that CONTRIBUTING.md shows in "Add a lesson in 5 steps", step 3. (The include lines
  are not written out here on purpose: the build also reads include lines inside
  comments, and it reports an error when the file they name does not exist.)

  A fragment that is not a complete program may be written inline, but only if it
  has five lines or fewer. A program that must fail uses the suffix .fail.cpp.
-->

<!--
  CALLOUTS: use them sparingly (at most about one per 300 words, never two in a row,
  never with a complete program inside). Allowed kinds: NOTE, TIP, WARNING, DANGER,
  BEST-PRACTICE, KEY-INSIGHT, ADVANCED. A callout is a block quote whose first line
  names its kind. The syntax (without the indentation shown here) is:

    > [!TIP]
    > Text of the callout.

    > [!BEST-PRACTICE]
    > Text of the callout.
-->

<!--
  TABS: when instructions depend on the reader's system or tools, use tabs with
  exactly one of these label sets, and the same information in the same order:
  Windows | macOS | Linux      or      Visual Studio | VS Code | Command line
  Every marker stands alone at the start of a line (without the indentation shown here):

    {{#tabs}}
    {{#tab Windows}}

    **Install:** Text for Windows.

    {{#endtab}}
    {{#tab macOS}}

    **Install:** Text for macOS.

    {{#endtab}}
    {{#endtabs}}

  KEYS: write keyboard keys as <kbd>Ctrl</kbd>+<kbd>F5</kbd>.
-->

<!--
  DIAGRAMS: use Mermaid, top to bottom, with short labels, and put one plain
  sentence that describes the diagram just before it.
-->

<!--
  CHECK YOUR UNDERSTANDING (optional): a collapsible question with a nested answer.
  Keep the empty lines, and do not indent anything:

    <details>
    <summary>Check your understanding</summary>

    The question.

    <details>
    <summary>Answer</summary>

    The answer.

    </details>

    </details>
-->

## Summary

<!--
  SUMMARY: three to six bullets that restate the main points of the lesson.
-->

- First main point.
- Second main point.
- Third main point.

<!--
  FURTHER READING (optional): primary sources only (the standard, cppreference,
  compiler and tool documentation), as https links. Delete this section if unused.
  Do not write previous and next links by hand: every page gets them from the book.
-->

## Further reading

- [Title of a primary source](https://en.cppreference.com/)
