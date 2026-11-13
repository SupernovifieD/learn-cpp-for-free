# 0.8 A few common C++ problems

Almost everyone hits a problem when they first set up a C++ toolchain, and the messages can look intimidating. This lesson lists the problems that beginners meet most often. Each one has the same three parts: the **symptom** you see, the **cause** behind it and the **fix**.

## The problems

Compilers word their messages differently, so the examples below show the kind of message to expect, not the exact text. If your message looks a little different, look for the same key phrases.

### The console window opens and immediately closes

**Symptom:** A console window flashes on the screen, and you cannot read the output.

**Cause:** The program finished, so its window closed with it. This happens when you start the program by double-clicking it, or from an IDE command that does not pause at the end.

**Fix:** Run the program from a terminal, where the output stays on screen after the program ends. In Visual Studio, use **Debug > Start Without Debugging** (<kbd>Ctrl</kbd>+<kbd>F5</kbd>), which keeps the window open until you press a key.

### The compiler is not found

**Symptom:** The terminal says that a command was not found, with `g++` or `clang++` as the name. On Windows, it says that `cl` is not recognized as an internal or external command.

**Cause:** The compiler is not installed, or the terminal does not know where it is. A terminal finds programs by searching a list of folders called the **PATH**. Microsoft's `cl` is only available inside a Developer Command Prompt, which sets up the PATH for you.

**Fix:** Install the compiler as lesson 0.6 describes, then open a new terminal window, because terminals read the PATH when they start. On Windows, use **Developer Command Prompt for Visual Studio**. Check again with `g++ --version`, `clang++ --version` or `cl`.

### Errors in a program you typed from the book

**Symptom:** The compiler reports errors for code that looks exactly like the code in the lesson.

**Cause:** Usually a small typing mistake. The usual suspects are a missing semicolon, a brace that is not closed, a letter in the wrong case, and curly quotation marks, which word processors and some websites insert in place of plain ones. For a missing semicolon, the message says that a semicolon was expected, and it points at the end of the line, so look at the line before the one where the compiler complains. For curly quotes, the message complains about an unexpected character or a character that is not valid in an identifier.

**Fix:** Compare your code with the lesson one character at a time, retype any line you doubt, and write code in a code editor, as lesson 0.4 advised.

> [!TIP]
> Read the first error first. One mistake often causes a long list of later errors, and fixing the first one can make all the others disappear. Recompile after each fix.

### The linker cannot find main

**Symptom:** The build gets as far as linking and then fails with a message about `main`. GCC says there is an undefined reference to `main`, Clang on macOS says that the symbol `_main` is undefined, and Microsoft's linker reports an unresolved external symbol with the error code LNK2019.

**Cause:** The linker needs `main` to know where the program starts. The function may be missing, or misspelled, because C++ is case-sensitive and `Main` is a different name from `main`. The file that contains `main` may also not be part of the build.

**Fix:** Spell it `main` in lowercase. Check that the file is listed in your project, or named in your command line.

### More than one main

**Symptom:** The link step fails and complains that `main` is defined more than once. GCC reports a multiple definition, Clang on macOS reports a duplicate symbol, and Microsoft's linker reports error LNK2005, which means that a symbol is already defined.

**Cause:** Two source files in the same build each contain a `main` function. This often happens when you keep every exercise in one project.

**Fix:** A program has exactly one `main`. Give each exercise its own project or its own folder, or remove the extra `main`.

### A missing include

**Symptom:** The compiler reports an error on a line that uses `std::cout`. GCC says that `cout` is not a member of `std`, and Clang says that `std` is not declared.

**Cause:** You used a part of the Standard Library without including the header that provides it. This program shows the mistake:

```cpp title="missing-include.cpp"
{{#include ../../examples/ch00/08-missing-include.fail.cpp}}
```

The first line is a comment that records why the program fails, and the book's automated checks read it. The compiler has never heard of `std::cout`, because nothing told it where to find it.

**Fix:** Add `#include <iostream>` at the top of the file, as the program in lesson 0.7 does.

### A .c file compiled as C

**Symptom:** The compiler cannot find a header such as `iostream`, with a message like "file not found", even though your code is correct.

**Cause:** Your file's name ends in `.c`. Compilers treat that ending as C code, and C has no `iostream`. Microsoft's compiler follows the same rule, and the GNU C++ driver `g++` accepts `.c` files as C++, while Clang's C++ driver warns that doing so is deprecated.

**Fix:** Rename the file so that it ends in `.cpp`.

### Antivirus software quarantines your program

**Symptom:** The executable disappears after a build, or it refuses to start, and your security software shows a notification.

**Cause:** Security software sometimes treats a program it has never seen before, which includes every program you build yourself, as suspicious.

**Fix:** Open your security software, look in its quarantine or protection history, and restore the file if it is the program you built. Most products let you allow one folder, such as the folder that holds your projects.

> [!WARNING]
> Do not turn off your protection completely. Allow your projects folder only, and only for programs that you wrote.

## How to search for an error message effectively

Searching the web for an error message is a normal part of programming. A few habits make it work much better:

1. Copy the key part of the first error message, without your file names, line numbers and variable names, because those are specific to your computer.
2. Add the name of your compiler, such as GCC, Clang or MSVC, since each one words its messages differently.
3. Search for the message text in quotation marks, so the search engine looks for the whole phrase.
4. Prefer official documentation. Microsoft documents its compiler and linker error codes, such as those that begin with `C` or `LNK`, and cppreference explains the language and the Standard Library.
5. When you ask others for help, include your code, the full first error message and your compiler and its version.

## Summary

- Run console programs from a terminal, or use Start Without Debugging in Visual Studio, so the output stays visible.
- A "command not found" message means the compiler is missing or the PATH is wrong, and `cl` needs a Developer Command Prompt.
- Read the first error first, and check for typing slips such as missing semicolons and curly quotes.
- A link error about `main` means that `main` is missing or misspelled, or that the file is not in the build, and two definitions of `main` cause a different link error.
- A missing `#include` makes the compiler fail on names from the Standard Library, and a file that ends in `.c` is compiled as C.
- Security software can quarantine a new program, and restoring it is better than disabling your protection.
