# 0.7 Compiling your first program

You have your tools, so it is time to use them. In this lesson you build a small program that prints a greeting, run it, and see exactly what a successful build looks like. The program does very little, and that is the point: it lets you test the whole toolchain before anything complicated gets in the way.

## Projects and console applications

An IDE organizes your work into **projects**. A project is a collection of source files and settings that the IDE uses to build one program. Visual Studio, for example, creates a project when you start a new program, and Visual Studio Code and the command line work with plain folders instead.

Every program in this book is a **console application**, which is a program that reads and writes text in a console window and has no graphical interface of its own. Console applications are the simplest kind to write, so they keep your attention on the language.

## The program

This is the program. Type it into a new file named `hello-world.cpp`, rather than pasting it, as the tip in lesson 0.1 suggests.

```cpp title="hello-world.cpp"
{{#include ../../examples/ch00/07-hello-world.cpp}}
```

You will learn how each line works in [lesson 1.1](../ch01-cpp-basics/01-statements-and-the-structure-of-a-program.md), so this is only a first orientation:

- `#include <iostream>` makes the tools for printing text available to your program.
- `int main()` marks the place where your program starts running. Every C++ program has one `main`.
- The braces `{` and `}` mark the beginning and the end of the code that belongs to `main`.
- `std::cout << "Hello, world!\n";` prints the text between the quotation marks, and the `\n` at its end starts a new line.
- `return 0;` tells the operating system that the program finished successfully.

## Building and running

Building means turning your source file into an executable, as lesson 0.5 described. Choose the tab that matches the tools you installed. Each tab covers how to build the program and then how to run it.

{{#tabs}}
{{#tab Visual Studio}}

**Build:** On the start screen, choose **Create a new project**. Set the language to **C++** and the platform to **Windows**, select the **Console App** template and choose **Next**. Give the project a name and create it, then replace the code that Visual Studio generated with the program above. From the **Build** menu, choose **Build Solution**.

**Run:** From the **Debug** menu, choose **Start Without Debugging**, or press <kbd>Ctrl</kbd>+<kbd>F5</kbd>. A console window opens, runs your program and waits for a key press before it closes.

{{#endtab}}
{{#tab VS Code}}

**Build:** Install the C/C++ extension, then open an empty folder in Visual Studio Code and create `hello-world.cpp` in it. Open the integrated terminal with the **Terminal** menu, and build with the commands from the **Command line** tab. The official guides for each platform, which are linked in lesson 0.6, show how to build with a Visual Studio Code task instead.

**Run:** Start the program from the integrated terminal, as the **Command line** tab shows.

{{#endtab}}
{{#tab Command line}}

**Build:** With GCC or Clang, run one of these commands in a terminal, in the folder that holds your file. The `-std=c++20` option selects the language standard, and `-o` names the executable.

```bash
g++ -std=c++20 -o hello-world hello-world.cpp
clang++ -std=c++20 -o hello-world hello-world.cpp
```

With Microsoft's compiler, open a **Developer Command Prompt for Visual Studio** and run the equivalent command. The `/std:c++20` option selects the standard, `/EHsc` enables standard C++ exception handling, and `/Fe:` names the executable.

```powershell
cl /std:c++20 /EHsc /Fe:hello-world.exe hello-world.cpp
```

**Run:** On Linux and macOS, start the program by its path. On Windows, enter its name.

```bash
./hello-world
```

```powershell
hello-world
```

{{#endtab}}
{{#endtabs}}

## What success looks like

When the program runs, it prints a single line and finishes:

```text title="Output"
{{#include ../../examples/ch00/07-hello-world.out}}
```

If you see that line, your compiler, your editor and your setup all work, and you have built and run a real C++ program. Well done.

If the build fails or the output is different, do not worry. Almost everyone hits a problem during setup, and lesson 0.8 describes the most common ones along with their fixes.

## Summary

- An IDE groups your files and settings into a project, and every program in this book is a console application.
- `main` is where a C++ program starts, and you will learn the other lines of the first program in [lesson 1.1](../ch01-cpp-basics/01-statements-and-the-structure-of-a-program.md).
- Building turns your source file into an executable, and you run the executable to see the program work.
- Visual Studio builds with **Build Solution** and runs with <kbd>Ctrl</kbd>+<kbd>F5</kbd>, and the command line uses `g++`, `clang++` or `cl`.
- The program prints `Hello, world!` when it works, and lesson 0.8 helps if it does not.
