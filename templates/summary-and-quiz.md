<!--
  HOW TO USE THIS TEMPLATE
  1. Copy this file to docs/chNN-slug/x-summary-and-quiz.md. The file name always starts with x-,
     so the page sits after the numbered lessons.
  2. Replace every placeholder, then delete every comment like this one.
  3. Add the page to docs/SUMMARY.md as the last entry of the chapter, with the same label as the
     heading below, and add it to the list in the chapter's index.md.
  4. Put each solution program of the quiz in examples/chNN/x-qN-slug.cpp (or a project folder), with
     its .out file, or its .in and .session files if it reads input, exactly as for a lesson.
  5. Read CONTRIBUTING.md, then run: make check
-->

<!--
  HEADING: exactly one level-1 heading, written as "<chapter>.x Chapter <chapter> summary and quiz".
  It must be identical to the page's label in docs/SUMMARY.md.
-->

# N.x Chapter N summary and quiz

<!--
  OPENING PARAGRAPH: 2 to 4 sentences. Say what the page recaps and how to use the quiz: try each
  question before you open its solution.
-->

Say in two to four sentences what this page recaps and how to use the quiz.

## Summary

<!--
  SUMMARY: one short paragraph or bullet group for each lesson of the chapter, in lesson order. Link
  each lesson with a relative link to its file, and restate its key terms in plain words (bold is only
  for the place where a term is defined, in the lesson). Do not teach anything new here.
-->

- [N.1 First lesson](01-first-lesson.md): Restate the key terms of the lesson in one or two sentences.
- [N.2 Second lesson](02-second-lesson.md): Restate the key terms of the lesson in one or two sentences.

## Quiz

<!--
  QUIZ: 5 to 8 questions in rising difficulty. At least half of them are programming tasks with a
  solution program that is checked like every other example. A question is a level-3 heading,
  "Question 1", "Question 2" and so on, followed by the question as normal, visible text. The
  solution goes into a collapsible below it, so the reader tries first. Keep the empty lines and do
  not indent anything.

  For a programming task, the solution explains the idea in a few sentences and then includes the
  program, and its Output block (or its Example session block, when the program reads input), the
  way a lesson does: see "Add a lesson in 5 steps" in CONTRIBUTING.md. (The include lines are not
  written out here on purpose: the build also reads include lines inside comments, and it reports an
  error when the file they name does not exist.)

  The structure of every question:

    ### Question 1

    The question.

    <details>
    <summary>Solution</summary>

    The explanation, and for a programming task the solution program.

    </details>
-->

### Question 1

Write the first question here.

<details>
<summary>Solution</summary>

Explain the solution here.

</details>
