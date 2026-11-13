# 0.11 Configuring your compiler: Warning and error levels

A compiler can tell you about far more than the mistakes that stop a build. With the right options, it also points out code that is legal but suspicious, and it can refuse to continue until you fix that code too. This lesson explains how, and it shows the exact options that this book uses for every example.

## Errors and warnings

The compiler reports two kinds of problems. An **error** means that the code breaks the rules of the language, so the compiler cannot produce a program. A **warning** means that the code is legal, but it looks like a mistake, so the compiler builds the program anyway and tells you about it.

It is tempting to ignore warnings, because the program still runs. That is exactly why they deserve attention. A warning often points to a real bug, such as a variable you never use, or a number that gets silently changed when it is converted to another type.

Compilers can **treat warnings as errors**, which stops the build until you fix every warning. Working this way is a habit worth building from the beginning, because a build with no warnings makes every new warning stand out.

## The options this book uses

Every complete program in this book is built with these options, using both GCC and Clang. They are stored in a single file in the book's repository, and the book's automated checks read that same file, so what you see here is exactly what is tested.

```bash title="flags-gcc-clang.txt"
{{#include ../../examples/flags-gcc-clang.txt}}
```

The options work like this:

| Option | What it does |
| --- | --- |
| `-std=c++20` | Selects the C++20 standard, without GNU extensions |
| `-Wall` | Turns on a large group of warnings about questionable code |
| `-Wextra` | Turns on more warnings that `-Wall` leaves out |
| `-Wpedantic` | Warns about code that does not follow the ISO standard, including extensions |
| `-Wconversion` | Warns about implicit conversions that may change a value |
| `-Wsign-conversion` | Warns about implicit conversions that may change the sign of an integer |
| `-Wshadow` | Warns when a local name hides another variable, parameter or type |
| `-pedantic-errors` | Reports code that does not follow the standard as an error |
| `-Werror` | Turns every warning into an error |

You do not need to understand every warning yet. Most of them will make sense once you have met the parts of C++ that they are about, and you can look the others up in the [GCC documentation](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html). Clang accepts the same options.

## Microsoft's compiler

Microsoft's compiler uses different spellings. `/W4` selects a high warning level, and `/WX` treats warnings as errors. Together with the options from the earlier lessons, a full command looks like this:

```powershell
cl /std:c++20 /EHsc /permissive- /W4 /WX hello-world.cpp
```

Its warnings are not identical to the ones from GCC and Clang, so a program can build cleanly with one and still produce a warning with another. If that happens, read the message and fix the code.

## An example: an unused variable

This program contains a variable that nothing uses:

```cpp title="unused-variable.cpp"
{{#include ../../examples/ch00/11-unused-variable.fail.cpp}}
```

The first line says that the program must fail with the book's options, and the second line says that it must build when `-Werror` is removed. That second line proves the point of the lesson: the program is legal C++, and the build fails only because warnings are treated as errors.

With `-Wall` on, the compiler warns about the unused variable. With `-Werror` also on, that warning stops the build, and you have to remove the variable or use it.

> [!KEY-INSIGHT]
> A warning that you fix today is a bug that you do not have to find tomorrow, and warnings as errors make sure that you cannot forget.

## Setting the options

{{#tabs}}
{{#tab Visual Studio}}

**Switch:** Open the project's property pages, choose **Configuration Properties**, then **C/C++**, then **General**. Set **Warning Level** to **Level4 (/W4)** and **Treat Warnings As Errors** to **Yes (/WX)**.

**Note:** Choose **All Configurations** first, as lesson 0.9 explained, so the settings apply to both Debug and Release.

{{#endtab}}
{{#tab VS Code}}

**Switch:** Add the options to the list of compiler arguments in your build task, in the same way as in lesson 0.10.

**Note:** Copy the options from the file above, one option per argument.

{{#endtab}}
{{#tab Command line}}

**Switch:** Add the options after the compiler name. This command builds the program from lesson 0.7 with all of them.

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Wshadow -pedantic-errors -Werror -o hello-world hello-world.cpp
```

**Note:** Replace `g++` with `clang++` to use Clang. Build tools, which lesson 0.5 introduced, let you write the options once instead of typing them each time.

{{#endtab}}
{{#endtabs}}

## Summary

- An error stops the build, and a warning reports code that is legal but suspicious.
- Treating warnings as errors forces you to fix every warning, which builds a good habit.
- The book builds every example with `-std=c++20 -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Wshadow -pedantic-errors -Werror`.
- With Microsoft's compiler, use `/W4` and `/WX`, together with the options from the earlier lessons.
- An unused variable is legal C++, but it stops the build when warnings are errors.

## Further reading

- [GCC documentation: warning options](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html)
- [Clang documentation: user's manual](https://clang.llvm.org/docs/UsersManual.html)
- [Microsoft documentation: warning level options](https://learn.microsoft.com/en-us/cpp/build/reference/compiler-option-warning-level)
