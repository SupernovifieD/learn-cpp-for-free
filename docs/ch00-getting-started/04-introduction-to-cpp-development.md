---
description: The steps of developing a C++ program, why a little design helps, what source files are, and how code editors differ from IDEs.
---

# 0.4 Introduction to C++ development

Writing code is only one step in making a program. This lesson walks through the whole process, from the problem you want to solve to a program you can trust, and it introduces the files and tools you will work with along the way.

## The development loop

Programmers repeat the same steps over and over. Here they are in order:

1. **Define the problem.** Decide in a sentence or two what the program should do, before you think about how.
2. **Design a solution.** Sketch how the program will work: what information goes in, what comes out, and what steps lie in between.
3. **Write the code.** Turn the design into C++ source code.
4. **Compile.** Use a compiler to translate the code into a form the computer can run, and fix any mistakes it reports.
5. **Link.** Combine the compiled pieces and any libraries into one program.
6. **Test.** Run the program with different inputs and check that it does what you intended.
7. **Debug.** When it does not, find the cause and fix the code.
8. **Repeat.** Go back to whichever step the problem points to.

!!! key-insight "Key insight"
    This is a loop, not a straight line. Experienced programmers go around it many times, often within minutes, so mistakes are cheap to find when you check your work often.

You will meet compiling and linking in the next lesson. For now, remember that they are separate steps, even though tools often run them together when you press a build button.

## Why a little design saves time

It is tempting to start typing code right away. Code written without a plan tends to solve the wrong problem, or to grow into a tangle that is hard to repair, so a few minutes of thinking first often saves much more time later.

Suppose you want a program that converts a temperature from Celsius to Fahrenheit. Before writing any code, you can answer a few questions on paper:

- Where does the temperature come from?
- What should the program print?
- What is the formula that connects the two scales?

Once you have written down the answers, the code almost writes itself. Make a habit of describing, in plain words, what a program must do, what goes in and what comes out before you write any code.

## Source files

Source code lives in text files called **source files**. By convention, C++ source files end in `.cpp`. Compilers accept other endings too, such as `.cc` and `.cxx`, but this book always uses `.cpp`.

A program usually grows to span several source files, and you will see how they work together in the next lesson. Some files hold code that several source files share. These are **header files**, and their names usually end in `.h` or `.hpp`. A later chapter explains headers in detail, so for now it is enough to know that they exist.

Source files are plain text. They have no fonts, colors or hidden formatting, only the characters you typed.

!!! warning
    Never write code in a word processor. It saves extra formatting information that the compiler cannot read, and it may replace plain quotation marks with curly ones, which the compiler rejects.

## Editors and IDEs

You write source files in a **code editor**, which is a program for editing plain text. Most code editors color the different parts of your code, which makes it easier to read and helps you spot typing mistakes.

An **integrated development environment**, or **IDE**, goes further. It bundles an editor with other tools: code completion that suggests names as you type, underlines for mistakes, buttons that build and run your program, and a debugger for finding problems. Many programmers work in an IDE, and many others prefer a lightweight editor and a terminal. Both approaches work well.

An IDE is not a compiler. The compiler is a separate program, and the IDE calls it on your behalf. Lesson 0.6 helps you install the tools you need, and lesson 0.7 uses them to build your first program.

## What comes next

Lesson 0.5 explains what happens when a compiler and a linker turn your source files into a program. After that, you will install your tools and run real code.

## Summary

- Developing a program is a loop of defining the problem, designing, writing, compiling, linking, testing and debugging.
- A few minutes of design before coding usually saves time later.
- C++ source files are plain text, usually ending in `.cpp`, and header files usually end in `.h` or `.hpp`.
- Write code in a code editor or an IDE, never in a word processor.
- An IDE bundles an editor, build tools and a debugger, but it is not the compiler.

## Further reading

- [GCC documentation: file name suffixes and overall options](https://gcc.gnu.org/onlinedocs/gcc/Overall-Options.html)
