# Contributing to The C++ Book

Thank you for helping. This guide explains how to set up your computer, how to add a lesson or a chapter, and the rules that keep the book consistent. A new lesson should need only Markdown and C++ files: you never have to touch the theme, the workflow or the scripts.

## Ground rules

- **Write everything yourself.** Do not copy or closely paraphrase text, examples or images from other books or websites. Check facts against primary sources such as cppreference.com, isocpp.org and the GCC, Clang and Microsoft documentation.
- **Keep it simple.** Plain Markdown on top of mdBook's own look. The only additions are one small stylesheet and script in `theme/` and one preprocessor, `scripts/mdbook_cppbook.py`. No copies of mdBook's templates, and no other plugins unless a lesson cannot be written without them.
- **Never weaken a check** to make it pass. Fix the cause instead.

## Set up your computer

You need Python 3.11 or newer, `make`, Git and a C++ compiler. The example checker builds every program with both GCC and Clang, so install both if you can. You do not need Rust: mdBook is a single program that `make install` downloads.

**macOS and Linux**

```bash
git clone https://github.com/SupernovifieD/learn-cpp-for-free.git
cd learn-cpp-for-free
make install
```

`make install` downloads mdBook and mdbook-mermaid at the versions pinned in `scripts/install_tools.py` into `.tools/` (it checks each download against a SHA-256), creates a virtual environment in `.venv` for the test tools, installs the pinned packages and downloads the browser that the UI tests use.

**Windows (PowerShell)**

`make` is often missing on Windows, so run the commands directly. After the setup below, activate the virtual environment with `.venv\Scripts\Activate.ps1`, so that `python` in the table points at it, and put the tools on your path with `$env:PATH = "$PWD\.tools\bin;$env:PATH"`.

```powershell
git clone https://github.com/SupernovifieD/learn-cpp-for-free.git
cd learn-cpp-for-free
py -3 scripts/install_tools.py
py -3 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python -m playwright install chromium
```

| Task | `make` target | Command without `make` |
| --- | --- | --- |
| Preview the book | `make serve` | `mdbook serve` |
| Build the book | `make build` | `mdbook build` |
| Lint the content | `make lint` | `python scripts/lint_content.py` |
| Check the examples | `make examples` | `python scripts/check_examples.py` |
| Test the example checker | `make test-scripts` | `python -m pytest tests/scripts` |
| Check formatting | `make format-check` | `clang-format --dry-run --Werror` on every `.cpp` and `.h` file in `examples/` |
| Browser tests | `make test-ui` | `mdbook build`, then `python -m pytest tests/ui -n 2 --dist loadscope` |
| Screenshots | `make screenshots` | `mdbook build`, then `python tests/ui/screenshots.py` (options: `--open-details`, `--only <text>`, `--widths 320,768`) |

Two details of `mdbook build`: it prints a note that mdbook-mermaid was built against an earlier 0.5 release, which is expected, and it exits successfully even when an include names a missing file, so `make build` also fails when its log contains a `WARN` or `ERROR` line.

**A note about GCC on macOS.** The `g++` command on macOS is Apple's Clang. The example checker detects this, does not count it as GCC and prints a warning. To check with real GCC, install it (for example with Homebrew) and point the checker at it: `GXX=g++-15 make examples`. CI always checks with real GCC. Also on macOS, the system scans every newly built program, so its first start can take a few seconds. The checker therefore starts a program that exceeds the time limit once more, and reports it only when it is too slow both times.

## Daily workflow

1. Create a branch from `main`.
2. Run `make serve` and edit files. The browser reloads when you save, also when you change a file in `examples/`.
3. Run `make check` before you commit. It runs, in order: the content lint, the tests of the example checker, the example check, the format check, the build and the browser tests. CI runs the same commands.
4. Open a pull request. The checklist in the pull request template mirrors this guide.

`make format` reformats the C++ examples with the pinned `clang-format`, so everyone formats the same way. `make screenshots` saves pictures of every page to `artifacts/screenshots/` for the visual review described below.

## Add a lesson in 5 steps

Suppose you are adding lesson 0.14, "Example lesson".

1. **Copy the template.** Copy `templates/lesson.md` to `docs/ch00-getting-started/14-example-lesson.md`. Lesson files are named `NN-slug.md`, with a two-digit number and a kebab-case slug. The first heading must be the label you will use in the table of contents, such as `# 0.14 Example lesson`. Pages have no front matter: the file starts with its heading. Then write the lesson: replace every placeholder with real text and delete every comment from the template. `make lint` rejects a page that still contains template text.
2. **Write the example programs.** Put each complete program in `examples/ch00/14-example-lesson.cpp` and its exact expected output in `examples/ch00/14-example-lesson.out`. Run `make format` and then `make examples`, and fix everything they report. If the output differs between machines, change the program so that it does not, because every output the book shows is checked (see "Output must not depend on the platform" under "Rules for examples").
3. **Include the programs in the lesson.** Never paste a complete program into a lesson. Include the file, and its output, with `{{#include}}`. The path is relative to the page, so from a lesson in `docs/ch00-getting-started/` it starts with `../../examples/`:

    ````markdown
    ```cpp title="example-lesson.cpp"
    {{#include ../../examples/ch00/14-example-lesson.cpp}}
    ```

    ```text title="Output"
    {{#include ../../examples/ch00/14-example-lesson.out}}
    ```
    ````

    The `title` is the label above the block: a file name is shown as "Filename: example-lesson.cpp", and any other title, such as `Output`, as written. An inline fragment of five lines or fewer may be written in the fence itself, with or without a title. Always give a fence a language (`cpp`, `bash`, `powershell`, `text`). A line of code that is too wide scrolls inside its block.
4. **Add the page to the table of contents.** In `docs/SUMMARY.md`, add a line under the chapter, indented by two spaces, with the same label as the lesson's first heading:

    ```markdown
    - [0.14 Example lesson](ch00-getting-started/14-example-lesson.md)
    ```

    Also add the lesson to the list in the chapter's `index.md`. Order in `SUMMARY.md` is the reading order and the order of the previous and next arrows.
5. **Check, review and commit.** Run `make check`. Then run `make serve` or `make screenshots`, look at your page (see the visual checklist below), and commit with a message such as `docs(ch00): add lesson 0.14`.

## Add a chapter

1. Create the folder `docs/chNN-slug/` with a two-digit chapter number.
2. Copy `templates/chapter-index.md` to `docs/chNN-slug/index.md` and fill it in. Open with a concept map that connects the chapter's main ideas, before the lesson list.
3. Add the chapter to `docs/SUMMARY.md`. The chapter's `index.md` is the chapter's own entry, and its lessons are indented by two spaces under it:

    ```markdown
    - [1. Chapter title](ch01-slug/index.md)
      - [1.1 First lesson](ch01-slug/01-first-lesson.md)
    ```

4. Add the chapter to the contents list on the home page (`docs/index.md`).
5. Create `examples/ch01/` for the chapter's programs, and then add the lessons as described above.
6. End the chapter with a summary and quiz page (see the next section).

## Add a summary and quiz page

A chapter can end with a page that recaps its lessons and tests the reader.

1. **Copy the template.** Copy `templates/summary-and-quiz.md` to `docs/chNN-slug/x-summary-and-quiz.md`. The `x-` keeps the page after the numbered lessons. The first heading is the label in `docs/SUMMARY.md`, written like `1.x Chapter 1 summary and quiz`.
2. **Write the summary.** Under `## Summary`, write one short paragraph or bullet group for each lesson, in lesson order. Each links to its lesson and restates its key terms in plain words. Teach nothing new here.
3. **Write the quiz.** Under `## Quiz`, write 5 to 8 questions in rising difficulty. Each is a `### Question N` heading, the question as normal visible text, and the solution inside a `<details>` whose summary is `Solution`. At least half of the questions are programming tasks, and at least two ask the reader to read or predict a visual. Their solution programs are named `x-qN-slug` (`examples/ch01/x-q5-theater-seats.cpp`, or a project folder), checked like every other example, and included in the solution together with their Output or Example session block.
4. **Add the page** to `docs/SUMMARY.md` as the last entry of the chapter, and to the lesson list in the chapter's `index.md`.

On a quiz page the question stays visible and only the solution is collapsed. The nested question-and-answer pattern under "Callouts" is for the "Check your understanding" questions inside lessons.

## Rules for examples

- **Names.** `examples/chNN/NN-slug.cpp`, where `NN` is the number of the lesson that first uses the program. The programs of a chapter's quiz are named `x-qN-slug` instead, after the page `x-summary-and-quiz.md` that uses them. In a lesson, a single-file program is titled with its file name without the number prefix (`title="hello-world.cpp"`), and the files of a project keep their real names (`title="main.cpp"`).
- **Names in code.** Variables and functions use `camelCase` (`readNumber`, `totalSeats`). Global variables and global constants add the prefix `g_` (`g_visitorCount`); local constants have no prefix such as `k` or `c_`. A namespace that the book defines is one lowercase word (`pricing`, `geometry`). Loop counters are signed `int` values unless the lesson explains a reason otherwise, and descriptive names such as `pass`, `row` and `count` are preferred over `i` and `j` except in the shortest loops. Header files end in `.h`, and a header guard is named after its file in `UPPER_SNAKE_CASE` (`ADD_H` for `add.h`). Once the book has explained header guards, every header has one; a lesson that shows headers earlier says why it has none yet. Lesson 8.15's header is named `Random.h` and uses `RANDOM_H`. Write the literal suffixes `L`, `LL`, `UL` and `ULL` in capitals, because a lowercase `l` looks like the digit 1, and `u` and `f` in lower case (`5u`, `3.14f`). The book picks one style and says in its lesson about names that other styles exist.
- **Projects (programs with several files).** A program is either one file or a folder. A project is a folder such as `examples/ch02/08-two-files/` that holds the program's `.cpp` files and the `.h` headers they include, with one of the files named `main.cpp`. The checker compiles and links every `.cpp` file of the folder in one command. The folder is flat (no folders inside it), and a `.cpp` file inside it is never a program of its own. Headers are allowed only inside project folders, and they follow the same formatting rules as `.cpp` files.
- **Files that belong to a program** sit next to it, whether it is a file or a folder, never inside the project folder: `08-two-files.out` is the output of the folder `08-two-files/`. The exact expected standard output goes in `NN-slug.out`.
- **Programs that read input** have two more files. `NN-slug.in` holds what the reader types, one line for each press of the Enter key. `NN-slug.session` holds what the reader sees in the console: the program's output with the typed lines where they appear on the screen. For a program that prints `Enter a number: ` and then `Twice that is 14` after the reader types 7, the session is `Enter a number: 7` followed by `Twice that is 14` on the next line. The checker proves that removing each line of `.in`, in order, from where it appears in the session leaves exactly the program's output, so a wrong output line, a missing typed line and an input line that the session never shows are all errors. The proof covers the order of the typed lines and that everything else is the program's output. It does not check where a typed line sits, which should be right after the prompt that asks for it, and it cannot tell that the program really read every typed line. Place the lines as the program would show them, keep the input short, and say in the lesson what the reader types. A program has `.out` or `.session`, never both, and `.in` always goes with `.session`. Show a session in a block titled `Example session` (```` ```text title="Example session" ````) instead of `Output`, and write in the prose what the reader types ("Type 7 and press Enter").
- **Programs that write to the error stream.** A running program writes nothing to standard error, unless a file `NN-slug.err` next to it holds exactly what it writes there (debug output with `std::cerr` is the typical case). The `.out` (or `.session`) then shows the **console view**: standard output and standard error captured through one pipe, in the order the program wrote them, which is what a reader sees in a terminal (`std::cerr` is tied to `std::cout`, so the order is kept). The checker runs the program twice, once with separate pipes to compare the error stream with the `.err` file and once with one pipe to compare the console view with the `.out` or `.session` file. A lesson includes only the console view, titled `Output` or `Example session`, and says in the text which lines came from `std::cerr`. The `.err` file belongs to its program like `.in` and no page includes it. It is never empty, it always goes with a `.out` or `.session` file, and a program that must fail never has one.
- **Programs that halt with a status.** A running program normally has no `NN-slug.status` file and must return status 0. If a lesson intentionally ends it another way, put one integer from `0` through `255` in `NN-slug.status`, or put the word `abort` there when the program must terminate with `SIGABRT`. The checker requires that result from the ordinary and sanitizer runs, including the second run used for a merged console view. A status file works with `.out`, `.session` and `.err`, but never with a `.fail` or `.ub` program. State the status in the lesson's prose. The status file is checked but not included in the page.
- **Programs whose output varies.** Replace `.out` with a pair of files. `NN-slug.match` holds one Python regular expression per output line; every line the program prints must be a full match for the corresponding pattern, and the line counts must be equal. `NN-slug.example` holds one real console view captured from a run, and the checker proves that it matches the same patterns. Make patterns narrow enough to state the promise: use `[1-6]` for one die roll, not `.*`. The pair cannot be used with `.in`, `.session` or `.err`; keep varying-output programs simple. Include the `.example` file in the lesson in a block titled `Output (example)`. Never include `.match`, which is checker input rather than reader-facing output.
- **Programs that must fail.** Name a file `NN-slug.fail.cpp` and a project folder `NN-slug.fail/`. The first line of the file (of `main.cpp` for a project) must be `// expect-fail: <one-line reason>`. An optional second line, `// passes-without: <flag> [<flag> ...]`, makes the checker also prove that the program builds once those flags are removed, which shows that the failure comes from the flags the book teaches. A failing program never runs, so it has no `.out`, `.in` or `.session` file. The checker only knows that the build failed, so check yourself that it fails for the reason you describe. `make format` formats failing programs too, and `clang-format` cannot format code that does not parse: it may join two lines, because a missing semicolon turns two statements into one, or write `* /` for a stray `*/`. Read the file again after formatting, and choose a layout that the formatter leaves alone (a missing semicolon before a closing brace is one).
- **Programs that show undefined behavior.** A running program never has undefined behavior, and the book never shows output for it. A lesson that must show code whose behavior is undefined and that still compiles (a signed overflow, a view that outlives its string) uses a program named `NN-slug.ub.cpp`, or a project folder `NN-slug.ub/`. Its first line (the first line of `main.cpp` for a project) is `// undefined-behavior: <one-line reason>`; readers see it, so write a sensible comment. The checker never runs it without the sanitizers: it builds it with the strict flags minus `-Werror` (compilers often warn about exactly this bug, and that is fine) plus AddressSanitizer and UBSan, runs it with the lines of `NN-slug.ub.in` if that file exists, and requires a non-zero exit and a sanitizer report on standard error (`runtime error:` or `ERROR: AddressSanitizer`). A clean run fails with a message: choose an example that the sanitizers detect, or show a fragment of at most 5 lines, or describe the case in the text. The `.in` file is its only companion. A lesson includes it with the file name minus `.ub` (`title="overflow.cpp"`) and never with an `Output` block, describes what might happen without promising any result, and may say that the book's checks run the program under the sanitizers, which report the problem. A read of an uninitialized variable is not found by AddressSanitizer or UBSan, so show that as a `.fail` program that relies on a compiler warning. Without a sanitizer runtime the check is skipped with a warning on your computer, and CI fails; the `san` column of the row says `ub`.
- **Checked debugger walkthroughs.** A lesson that shows a GDB session uses two files next to a running program that reads no input. `NN-slug.gdb` holds the commands exactly as a reader types them at the `(gdb)` prompt, one per line, with no comments or blank lines, and with breakpoints on function names, never on line numbers. `NN-slug.gdb-expect` holds texts that GDB's output must contain, one per line, each found after the previous one; keep them free of addresses and of wording that changes between versions, such as `addPoints (current=40, bonus=2)` or `$1 = 42`. The checker builds the program with GCC, the strict flags and `-O0 -g`, runs `gdb -q -batch -nx -x NN-slug.gdb <program>` with a 30 second limit, and requires exit status 0 and every expectation (the `gdb` column). The lesson includes the `.gdb` file in a block titled `Commands for GDB` (```` ```text title="Commands for GDB" ````); the `.gdb-expect` file belongs to it like `.in`, and no page includes it. GDB's output goes into a pipe, where the program's own output is buffered and appears late, so the program's output is not part of what is checked. Without gdb the check is skipped with a warning on your computer (CI installs gdb and fails when it is missing). LLDB is not checked automatically.
- **Output must not depend on the platform.** CI checks output only on 64-bit Linux, but readers run the programs everywhere, so a checked `.out`, `.session` or `.err` file must be identical on 64-bit Windows (MSVC), macOS (Apple Clang, x86-64 and arm64) and Linux (GCC and Clang, x86-64 and arm64). Values that the standard leaves to the platform and that do differ there, such as `sizeof(long)`, `long double`, `wchar_t` and whether plain `char` is signed, go into the text or into a table that cites its source, never into checked output. So do digits that a library may print differently: choose values whose printing is the same everywhere. Output that intentionally changes by platform or run uses `.match` and `.example`; its patterns describe only the portable promise, while the example is clearly labeled as one run. You cannot run every platform, so check the facts in the standard or in the platform's documentation, and ask the reviewer to read the output files with this rule in mind.
- **Sanitizers.** The checker also builds every running program with AddressSanitizer and UBSan and runs it again with the same input, so a program with undefined behavior or a memory error fails even if it happened to print the right output (the `san` column of the result table). A program that shows undefined behavior on purpose is the one exception: it is named `.ub`, as described above. A compiler without a sanitizer runtime only gives a warning on your computer, so install the runtime that comes with your compiler to see the same results as CI, which requires it.
- **Every example is used.** Each file in `examples/` must be included by at least one page, or `make lint` fails. The exceptions are the files that belong to a program and are never shown: `.in`, `.err`, `.status`, `.match` and `.gdb-expect`, which must sit next to the program or walkthrough they belong to. A lesson shows a project as one titled block per file (`title="main.cpp"`, `title="add.h"`): headers first, then the other `.cpp` files, then `main.cpp`, then the output.
- **Formatting.** 4-space indent, braces on their own line, at most 80 columns, one statement per line, brace initialization, `"\n"` instead of `std::endl`. `make format` applies the rules from `.clang-format` to every `.cpp` and `.h` file.
- **The strict flags.** `examples/flags-gcc-clang.txt` holds the one line of compiler flags that CI uses and that lesson 0.11 shows. Change it only on purpose, because it changes what the book promises.

## Teach in order

An example or an explanation may use only what earlier lessons have taught. Think of a lesson's **toolbox**: everything the lessons before it taught, plus what the lesson teaches itself. Before you write an example, list what it uses and check every item against the toolbox. If an example needs something that is not in it, change the example or the order of the lessons, never the rule.

What each chapter adds to the toolbox is listed below. A chapter's examples may use its own list and every list before it; when you add a chapter, add its line. Lesson 0.13 is the one documented exception: its program prints the language standard with `const`, `long` and `if`, so that readers can run it before they know them, and the lesson says so.

- **Chapter 0:** `#include <iostream>`, `int main()`, `std::cout` with string literals and `"\n"`, `return 0`, and the compiler's commands and flags.
- **Chapter 1:** `int` variables and the forms of initialization, assignment, `std::cin`, `std::endl`, integer literals, `+ - * /` and unary minus, expressions, comments.
- **Chapter 2:** `void` and `int` functions, parameters, `return`, forward declarations, programs of several files, headers and header guards, namespaces and `::`, `EXIT_SUCCESS` and `EXIT_FAILURE` from `<cstdlib>`, and the preprocessor's `#include`, `#define`, `#ifdef`, `#ifndef`, `#if 0` and `#endif`.
- **Chapter 3:** `std::cerr` and debug output that the preprocessor switches on and off. The bugs in its programs are logic errors made from the toolbox so far: a wrong operator, swapped arguments, the wrong variable, whole-number division, a forgotten call, an unused result.
- **Chapter 4:** `short`, `long`, `long long` and their unsigned forms, `signed char` and `unsigned char`, `float`, `double`, `bool` with `true` and `false`, `char` with character literals and escape sequences, `sizeof`, the fixed-width types of `<cstdint>`, `std::size_t`, scientific notation, the `f` suffix, `std::setprecision`, `std::boolalpha`, logical NOT `!`, the comparison operators, `if`, `else` and `else if`, arithmetic on characters, and `static_cast`.
- **Chapter 5:** `const`, every literal suffix, the `s` and `sv` suffixes of string literals (with a using-directive inside a function), `0x`, `0b` and octal literals, digit separators, `std::hex`, `std::oct`, `std::dec`, `std::bitset`, `constexpr` variables, `std::string`, `std::getline`, `std::ws` and `std::string_view`.
- **Chapter 6:** precedence, associativity and grouping parentheses; unary `+`; `+=`, `-=`, `*=`, `/=` and `%=`; `%`; `std::pow` from `<cmath>`; prefix and postfix `++` and `--`; the comma operator; the conditional operator; all relational operators; `std::abs` from `<cmath>` and `std::max` from `<algorithm>` for approximate comparisons; `&&`, `||` and `!`.
- **Chapter 7:** nested blocks; user-defined and nested namespaces; namespace aliases; global variables; `static` for internal linkage and `extern`; inline functions and variables; inline `constexpr` variables in headers; static local variables; using-declarations and using-directives; unnamed and inline namespaces.
- **Chapter 8:** `if` with blocks; `if constexpr`; `switch`, `case`, `default` and `[[fallthrough]]`; `goto` in lesson 8.7 only; `while`, `do while` and `for`; `break` and `continue`; `std::exit`, `std::atexit` and `std::abort`; `std::mt19937`, `std::random_device`, `std::seed_seq` and `std::uniform_int_distribution die{1, 6};` from `<random>`; and `std::chrono::steady_clock` for seeding.
- **Not through Chapter 8:** arrays, `std::vector`, range-based `for`, references, pointers, enumerations, structures, classes, `auto`, user-defined templates, lambdas, exceptions, `std::format`, `std::print`, and handling a failed `std::cin` read.

A later feature may be named in prose with a forward reference ("You will meet `if` statements in Chapter 4"), but it never appears in a program that readers type or that the checker runs, and the lesson does not teach it in depth. Something that a lesson shows only to say that it is wrong goes into a `.fail` program. When you review a lesson, ask whether a reader who has read only the earlier lessons could follow every line.

## Writing style

- Write to "you", in a friendly, direct and precise tone, in American English.
- Keep paragraphs to four sentences or fewer, with one idea per section.
- Bold a term where you define it, and use it consistently afterwards.
- Never use "simply", "just", "obviously" or "easy".
- Put identifiers, file names and commands in backticks, UI labels in bold (**File > New > Project**) and keys in `<kbd>`, one element per key: `<kbd>Ctrl</kbd>+<kbd>F5</kbd>`.
- Point forward ("You will learn what `std::cout` is in Chapter 1") instead of over-explaining.
- Phrase facts that change, such as versions and menu names, so that they age well, and link the official page.
- No raw HTML and no emoji in pages. The only HTML allowed is `<details>`, `<summary>` and `<kbd>`, without attributes.
- Shell commands go in `bash` (or `powershell`) blocks without a `$` prompt, so the copy button copies a runnable command.

Every lesson starts with its heading and an opening paragraph that states the problem the lesson solves. In Chapter 6 and later, explain the idea with a visual before introducing its syntax or showing any C++ code; use the same names and values in the picture, prose and program. Show path, scope and lifetime pitfalls visually when those relationships are the point. End with 1 to 3 "Check your understanding" questions (at least one asks the reader to use a visual), a `## Summary` with 3 to 6 bullets, and an optional `## Further reading` that links primary sources over https. Do not write previous and next links by hand, because the book provides the arrows. Links to other pages are relative `.md` links (`[Conventions](../conventions.md)`, optionally with `#heading-id`); the linter checks that the page and the heading exist.

## Callouts

A callout is a block quote whose first line names its kind in capitals:

```markdown
> [!TIP]
> Type each example yourself instead of pasting it.
```

Use only these kinds, and use them sparingly: never two callouts back to back, about one per 300 words at most, and never put a complete program inside one.

| Kind | Use it for |
| --- | --- |
| `[!NOTE]` | Useful context that is not essential |
| `[!TIP]` | A handier way to do something |
| `[!WARNING]` | A common mistake or a surprise |
| `[!DANGER]` | Something that can lose data or damage a setup (rare) |
| `[!BEST-PRACTICE]` | A habit professionals follow, with the reason |
| `[!KEY-INSIGHT]` | The idea that makes a topic fall into place |
| `[!ADVANCED]` | An aside for readers who want more depth |

The first three are mdBook's own. `scripts/mdbook_cppbook.py` renders the other four with the same markup. A question with its answer is a pair of nested `<details>` elements, which start closed. Keep the empty lines and do not indent anything:

```markdown
<details>
<summary>Check your understanding</summary>

The question.

<details>
<summary>Answer</summary>

The answer.

</details>

</details>
```

The page "Conventions used in this book" shows every kind.

## Tabs

When instructions depend on the reader's system or tools, use tabs, and use only these two sets of labels, spelled exactly like this:

- Operating systems: `Windows`, `macOS`, `Linux`
- Toolchains: `Visual Studio`, `VS Code`, `Command line`

Every tab in a set holds the same kind of information in the same order, with bold labels such as **Install:** and **Check:**. Every marker stands alone at the start of a line, with an empty line after `{{#tab ...}}`:

```markdown
{{#tabs}}
{{#tab Windows}}

**Install:** Text for Windows.

{{#endtab}}
{{#tab macOS}}

**Install:** Text for macOS.

{{#endtab}}
{{#endtabs}}
```

In the browser the groups become tabs that work with the arrow keys, and a reader's choice applies to every group with the same labels, on every page. Without JavaScript, all tabs are shown one under another, each under its label. The linter rejects other labels, mixed sets and unbalanced markers.

## Visuals

A visual earns its place by showing a relationship that prose handles poorly: structure, space, time, paths or quantity. It does not decorate syntax or turn a sentence into boxes. Every Chapter 6 or later lesson and chapter index needs at least one visual; aim for at least two per lesson on average in each chapter. Across a multi-chapter contribution, use at least five catalog kinds. A chapter index opens with a concept map before its lesson list, and a lesson's first visual comes before its first C++ fence or source include.

Choose the form by the idea, using only this catalog:

| Kind | Form | Use it for |
| --- | --- | --- |
| Path | `flowchart TD` | Decisions, loops, short-circuiting and what happens next |
| Tree | `flowchart TD` | Expression grouping and precedence |
| Nested boxes | `flowchart TD` with subgraphs | Blocks, scopes, namespaces, files and translation units |
| Lifetimes | `sequenceDiagram` with activations | When automatic and static objects exist across calls |
| Calls | `sequenceDiagram` | Side effects, cleanup and halt order |
| States | `stateDiagram-v2` | A generator's state or a loop seen as states |
| Layout | `block-beta` | Memory regions and side-by-side comparisons |
| Chart | `{{#chart}}` | Growth, distributions, sequences and other quantities |
| Data table | `{{#table}}` | Program traces, truth tables and checked results |
| Fact table | Markdown table | Rules and sourced facts, never program output |

The catalog was tested with the bundled Mermaid at a 320-pixel viewport in light and dark themes. The smallest text was 15 to 16px for flowcharts, states and layouts, 12.4px for lifetime sequences, 12.8px for call sequences and 12.1px for the configured chart. Gantt charts stayed at 10px and timelines at 5.9px, so neither is allowed. Mindmaps render, but they do not show direction or containment as precisely as the approved trees and nested boxes, so they are outside the catalog. Do not introduce another Mermaid kind until its phone-width, theme and accessibility behavior has been added to the pilot and tests.

All Mermaid configuration belongs in `theme/mermaid-init.js`, with presets for light and dark themes. A page never contains `%%{init}%%`, custom colors or styles. The preset controls flowchart spacing, sequence sizing, chart dimensions and theme-aware colors; meaning must not depend on color. The UI tests require at least 3:1 contrast for chart marks and at least 12px text after scaling.

Keep one idea in each visual, at most about 12 nodes, at most two nodes per flowchart row, and labels to about four words. An operator-only label uses a backslash escape such as `\*`, or a phrase such as `b * c`; never use an HTML entity code such as `#43;` or `&#42;`. Flowcharts, sequences and state diagrams have `accTitle` and `accDescr` lines that state the picture's point. The bundled `block-beta` grammar does not accept those keywords, so its surrounding prose supplies the accessible explanation.

Put a plain prose sentence immediately before every visual to say what it shows, and a sentence immediately after it to say what to notice. Names and values in the picture match the nearby prose and program. A reader who skips the code should still be able to explain the idea from the picture and its two sentences. At least one "Check your understanding" question in each lesson asks the reader to follow a path, complete a trace, choose a tree or otherwise use a visual.

### Charts and generated data tables

Every number that describes a program comes from a checked companion file, never from a hand-written Markdown table. Use these directives on one complete line:

```markdown
{{#chart bar ../../examples/ch06/03-values.out x="Input" y="Remainder" caption="Remainders by input"}}
{{#table ../../examples/ch06/03-values.out header="Input | Remainder"}}
```

A data file is an `.out`, `.err` or `.example` companion. Add `skip=N` to ignore `N` leading lines. A chart file has one `<label> <number>` row per point and at most 12 rows; use `bar` only when every value is non-negative, because the generated y-axis starts its bars at zero, and use `line` for negative values. Both axis titles and the caption are required. A chart made from `.example` output automatically adds "(one example run)" to its caption, and every chart is followed by an expandable table containing the same values.

A generated table splits each data line on whitespace into exactly as many fields as its `header` has columns. It has 1 to 3 columns and at most 16 rows. A hand-written Markdown table is only for facts backed by a primary source; keep it to three columns with short cells, and split a wider idea into two tables.

Include the program that produced chart or table data on the same page, normally or inside `<details>` with a summary such as "The program behind this chart". Because concept comes first, place the visual before that program in Chapter 6 and later lessons. The linter treats the directive's data file as used and rejects a missing companion or a program not shown on the page. The preprocessor stops the build for invalid fields, too many rows or columns, a non-number in a chart, or negative bar data.

### Visual lint and review

The linter requires the Chapter 6+ visual and concept-first order. Book-wide, it also requires a plain lead-in sentence, forbids page-local Mermaid configuration and numeric entity codes, and checks directive syntax and provenance. A passing automated test is not a visual review: use the screenshot process below and look at every result yourself.

## Debugger lessons

Lessons about a debugger use the Toolchains tabs (`Visual Studio`, `VS Code`, `Command line`), and every tab uses the same bold labels in the same order, for example **Start:**, **Step into:**, **Step over:**, **Step out:** and **Stop:**. The Command line tab covers GDB (Linux, and Windows through MSYS2) and LLDB (macOS) side by side in a table of at most three columns (Action, GDB, LLDB), next to the checked `Commands for GDB` block. Write keys with `<kbd>`, describe windows and panels by name, and take no screenshots. Check every key, menu and window name against Microsoft's current documentation and link its official page, because those names change. Debug builds use `-g -O0` on the command line and the Debug configuration in Visual Studio. You may quote a short value exactly as the debugger prints it (`$1 = 42`) when a `.gdb-expect` file proves it.

## Browser tests and visual review

`make test-ui` builds the book and opens every page in a headless browser at nine widths (320 to 1920 pixels) in light and dark mode, served under the same path as on GitHub Pages. The list of pages comes from `docs/SUMMARY.md`, and a listed page that was not built is an error. It checks, among other things, that:

- the page never scrolls sideways, neither does the text area inside it, and nothing sticks out of the text column,
- long code lines scroll inside their own block,
- there are no console errors or failed requests,
- axe-core finds no serious or critical accessibility problems (`tests/ui/axe_allowlist.json` is empty; an entry needs a written reason),
- every page has one `h1` in its content and no skipped heading levels,
- keyboard focus is visible on the controls readers use,
- the previous and next arrows follow `SUMMARY.md`, and the sidebar, search, theme menu and edit links work,
- tabs have the right roles, work with the keyboard, remember the choice and stay readable without JavaScript,
- answers stay hidden until opened, and the copy button copies the program in `examples/`,
- every page with a question is measured again with every `<details>` opened (nested ones too) at 320, 375 and 1280 pixels, so code, tables and diagrams inside answers are checked like the rest of the page, and axe-core checks the opened answers as well,
- every Mermaid diagram, found in the built pages, draws in both themes at 320 and 1280 pixels, keeps its text at 12 pixels or more, contains no placeholder or garbage text, and clips no text outside its SVG,
- every chart mark has at least 3:1 contrast against its background in both themes,
- an unknown address shows the book's own 404 page, styled and with a working sidebar.

When a check fails, the test run saves a screenshot of the failing page to `artifacts/screenshots/failures/`, and CI uploads that folder. Optional settings: `UI_WORKERS` sets how many browsers run in parallel (`make test-ui UI_WORKERS=4`, default 2), and `BASE_URL` tests a published book instead of the local build, for example `BASE_URL=https://supernovified.github.io/learn-cpp-for-free/`. While you draft a chapter, `make test-ui UI_ONLY=ch03-debugging` runs only the tests whose id contains that text (page ids start with the chapter folder and the lesson file, so `UI_ONLY=ch03-debugging__04` is lesson 3.4). It is a drafting aid only: `make check` refuses it and CI never sets it, so every gate runs every page.

Automated checks do not see everything, so look at the screenshots of every new or changed page at 375 and 1280 pixels in both color schemes. Also use 320 for a page with a visual, tab, table or project. For a page with questions, look twice: once with the answers closed, and once with every answer opened (`make screenshots SCREENSHOT_ARGS="--open-details --only ch01"` saves the second set next to the first, with `-open` in the file name). Check that:

1. callouts line up with the text, and the custom kinds look like the built-in ones;
2. the copy button never covers code, and file names line up with the block edges;
3. output blocks look different from code but line up with it;
4. tab labels sit on one line and nothing is clipped on a phone;
5. long sidebar titles wrap cleanly and the current page is clearly highlighted;
6. the arrows at the bottom of the page do not overlap the text on a phone;
7. tables have an aligned header row and padded cells;
8. there is no doubled or collapsed spacing, for example between a heading and a callout;
9. the dark theme has no white boxes and no dark-on-dark text;
10. the menu bar never collides at 320 to 414 pixels;
11. rendered keys do not disturb the line height;
12. no text is smaller than 12px, and inline code is legible in both themes;
13. every visual has all of its text, with no garbage characters or missing labels;
14. labels stay inside the visual at every edge, do not overlap, and arrows do not cross needlessly;
15. chart bars and lines are visible in both themes, and every bar starts at zero;
16. a chart's last x-axis label is not cut off, and its plot surface does not clash with the page in a dark theme;
17. each visual says the same thing as the prose and checked program beside it; and
18. the idea remains understandable from the visual and its surrounding sentences without reading the code.

## Content checklist

Before you open a pull request, check that:

1. the wording is original, with nothing copied or closely paraphrased;
2. every fact that can change was checked against a primary source today;
3. the lesson covers what it promises and does not teach later chapters in depth;
4. the central idea and its first visual appear before syntax and code;
5. every complete program is an included, checked example, and every output number in a visual comes through a directive;
6. every visual uses the right kind, matches the prose and program, and passed the visual review above;
7. each term is bolded once where it is defined, and used consistently afterwards;
8. callouts have the right kind and are not stacked or overused;
9. tabs use the exact label sets;
10. the length is reasonable and paragraphs have four sentences or fewer;
11. the lesson has 1 to 3 questions, including a visual question, and a 3 to 6 bullet summary;
12. further reading uses primary sources over https; and
13. a beginner can follow every instruction and explain the central idea from the visuals without guessing.

## Commits and pull requests

Use Conventional Commits, `type(scope): description`, with one coherent change per commit. Common types are `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `build`, `ci` and `chore`. Examples: `docs(ch00): add lesson 0.14`, `fix(theme): keep icons aligned in callouts`.

Do not commit the virtual environment, `.tools/`, the `book/` folder, screenshots, caches or secrets. Open a pull request against `main` and fill in the checklist. Every check must be green before it can be merged.

Found a factual mistake? [Open an issue](https://github.com/SupernovifieD/learn-cpp-for-free/issues/new?template=content-error.md) or use the edit button in the top right corner of the page.
