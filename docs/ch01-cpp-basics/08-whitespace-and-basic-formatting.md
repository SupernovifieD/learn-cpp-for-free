# 1.8 Whitespace and basic formatting

The compiler reads your program as a stream of small pieces, and it cares much less about how those pieces are laid out than a human reader does. That freedom is useful, because it lets you arrange code so that people can understand it quickly. In this lesson you learn where layout matters to the compiler, what choices you have, and how to let a tool do the formatting for you.

## What whitespace is

**Whitespace** is the name for characters that leave blank space: spaces, tabs and line breaks. The compiler uses whitespace to tell where one piece of a program ends and the next one begins. The pieces are called **tokens**, and they are the words, numbers, names and symbols that your code is made of.

Apart from that, the compiler mostly ignores whitespace. These two statements mean exactly the same:

```cpp
int bookCount{42};
int    bookCount   {   42 }  ;
```

The second line is ugly, but it is legal, and it is another reason why you want a consistent layout: the compiler will not help you to keep one.

## Where whitespace matters

Whitespace is not completely ignored. It matters in four places:

- **Between tokens that would run together.** `int bookCount` needs a space, because `intbookCount` would be read as one made-up name. Between a name and a symbol, such as `bookCount{42}`, a space is optional.
- **Inside a string literal.** A string literal is text between quotation marks, such as `"Hello"`, and lesson 1.9 explains literals in general. Everything between the quotation marks is printed exactly as written, including spaces. The text `"a   b"` has three spaces between the letters, and the output has them too.
- **At the end of a `//` comment.** A line comment continues until the end of the line, so the line break is what ends it, as lesson 1.2 explained.
- **Around a preprocessor directive.** A directive such as `#include <iostream>` must stay on a line of its own, and the line break ends it.

## Splitting a long string

A string literal cannot contain a line break. If you press <kbd>Enter</kbd> inside the quotation marks, the compiler reports an error. When a message is too long for one line of your editor, you split it into two literals instead, and the compiler joins neighboring literals into one:

```cpp title="joined-literals.cpp"
{{#include ../../examples/ch01/08-joined-literals.cpp}}
```

```text title="Output"
{{#include ../../examples/ch01/08-joined-literals.out}}
```

The first output statement has two literals, one on each line, and the output shows them as one sentence. The program does not add a space where the pieces meet, so the space after the comma at the end of the first piece is part of the text. The second statement shows that spaces inside a literal are kept.

## Layout choices

Most layout questions are matters of taste, and every programming team settles them in its own way. Three of them come up in every program.

**Where the braces go.** The two common styles differ in the place of the opening brace. This book puts it on a line of its own, which is called the **Allman style**:

```cpp
int main()
{
    return 0;
}
```

Many programmers keep the brace at the end of the line that opens the block:

```cpp
int main() {
    return 0;
}
```

**How far to indent.** Statements inside braces are moved to the right, so that the structure of the program is visible. The book indents by four spaces. Two spaces and tabs are also common. Do not mix tabs and spaces in the same file, because the code then looks different in editors with different tab widths.

**How long a line may be.** Long lines are hard to read and hard to compare side by side. The book keeps lines to at most 80 characters, which is why its code rarely needs to scroll sideways.

None of these choices is right or wrong. What matters is that a program uses one choice everywhere, because the eye then finds the structure without effort.

> [!BEST-PRACTICE]
> Pick one layout and keep it. When you work in someone else's program, follow the layout that is already there instead of mixing in your own.

## Let a tool format your code

You do not have to apply a layout by hand. A formatter reads your code and rewrites its whitespace according to a set of rules. The tool that this book uses for its own examples is **clang-format**, and most editors and IDEs can run it, or a formatter of their own, with a single command. The names of the menus can change between versions, so check your tool's documentation if a step does not match what you see.

{{#tabs}}
{{#tab Visual Studio}}

**Format:** Choose **Edit**, then **Advanced**, then **Format Document**, or press <kbd>Ctrl</kbd>+<kbd>K</kbd> and then <kbd>Ctrl</kbd>+<kbd>D</kbd>. To format only the lines that you selected, press <kbd>Ctrl</kbd>+<kbd>K</kbd> and then <kbd>Ctrl</kbd>+<kbd>F</kbd>.

**Style:** For C++ files, Visual Studio uses ClangFormat. When your project folder has a file named `.clang-format`, Visual Studio follows the rules in it.

{{#endtab}}
{{#tab VS Code}}

**Format:** Press <kbd>Shift</kbd>+<kbd>Alt</kbd>+<kbd>F</kbd> on Windows, <kbd>Shift</kbd>+<kbd>Option</kbd>+<kbd>F</kbd> on macOS or <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>I</kbd> on Linux. You can also open the Command Palette and choose **Format Document**.

**Style:** The formatter belongs to the extension for the language, so install the C/C++ extension from lesson 0.7 first. It follows the `.clang-format` file of your project when there is one, as the **Command line** tab describes, and a built-in style when there is not. The extension's documentation lists its settings.

{{#endtab}}
{{#tab Command line}}

**Install:** clang-format is a separate tool, and a compiler installation does not always include it. It is part of LLVM, and package managers offer it, for example `brew install clang-format` on macOS, `sudo apt install clang-format` on Debian and Ubuntu, and `pip install clang-format` on any system that has Python.

**Format:** Run `clang-format -i` followed by the name of your file. The `-i` option makes the tool change the file in place. Without it, the tool prints the formatted code and leaves the file alone.

```bash
clang-format -i hello-world.cpp
```

**Style:** The tool looks for a file named `.clang-format` in the folder of your source file and in the folders above it, and that file holds the rules. When it finds none, it uses the LLVM style, which indents by two spaces and keeps the opening brace on the line of the code that comes before it. To get the layout of this book, create a `.clang-format` file in your project folder with these four lines:

```text title=".clang-format"
BasedOnStyle: LLVM
IndentWidth: 4
BreakBeforeBraces: Allman
ColumnLimit: 80
```

A project that has such a file gets the same layout from every contributor.

{{#endtab}}
{{#endtabs}}

Formatting is something to run often, in the same way that you build often. A file that is formatted all the time never collects odd layouts that you have to fix later.

<details>
<summary>Check your understanding</summary>

**Question 1.** Do these two lines behave differently?

```cpp
int seats{40};
int seats {40} ;
```

<details>
<summary>Answer</summary>

No. The compiler ignores the extra spaces around the braces and before the semicolon, so both lines define the same variable. The first line is the one that a person reads more quickly.

</details>

**Question 2.** What does this statement print?

```cpp
std::cout << "tea" " for " "two\n";
```

<details>
<summary>Answer</summary>

It prints `tea for two` and a line break. The three neighboring literals are joined into one, and the spaces inside the second literal are kept.

</details>

</details>

## Summary

- Whitespace separates tokens, and the compiler otherwise mostly ignores it.
- Whitespace matters between tokens that would run together, inside string literals, at the end of a `//` comment and around preprocessor directives.
- A string literal cannot continue on the next line, but neighboring literals are joined into one.
- Brace placement, indentation and line length are choices, and consistency matters more than the choice.
- A formatter such as clang-format applies a layout for you, and every toolchain has a command for it.

## Further reading

- [ClangFormat (Clang documentation)](https://clang.llvm.org/docs/ClangFormat.html)
- [Options, Text Editor, C/C++, Formatting (Microsoft Learn)](https://learn.microsoft.com/en-us/visualstudio/ide/reference/options-text-editor-c-cpp-formatting)
- [Basic editing in Visual Studio Code: formatting](https://code.visualstudio.com/docs/editor/codebasics#_formatting)
