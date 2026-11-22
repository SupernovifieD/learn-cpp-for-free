# 3.x Chapter 3 summary and quiz

This page recaps the lessons of Chapter 3 and then tests what you remember. The summary names the key terms of each lesson, so use it to find a lesson that you want to read again.

The quiz has eight questions: the first four are about ideas, and the last four are programs. Two of the programs contain a bug for you to find and fix. Try each question before you open its solution.

## Summary

- [3.1 Syntax and semantic errors](01-syntax-and-semantic-errors.md): a syntax error breaks the grammar, a semantic error has a meaning that is invalid, and the compiler stops both. A logic error is valid code that does the wrong thing, and undefined behavior is the hardest kind to find.
- [3.2 The debugging process](02-the-debugging-process.md): reproduce the problem, find the root cause, understand it, decide how to fix it, repair the code and retest. The symptom is what you see, and the root cause is the mistake in the code.
- [3.3 A strategy for debugging](03-a-strategy-for-debugging.md): inspection means reading the code, and it fails because you read what you meant. Narrow a bug down by halves, test one hypothesis and change one thing at a time, and keep notes.
- [3.4 Basic debugging tactics](04-basic-debugging-tactics.md): switch code off to isolate a problem, trace calls, and print values. `std::cerr` is a separate, unbuffered stream that is tied to `std::cout`, and `2>` redirects it.
- [3.5 More debugging tactics](05-more-debugging-tactics.md): debug output between `#ifdef ENABLE_DEBUG` and `#endif` exists only when the macro is defined, for example with `-D` on the command line. Logging keeps messages for good, and the standard library has no logging facility.
- [3.6 Using an integrated debugger: Stepping](06-using-an-integrated-debugger-stepping.md): a debugger pauses a program and shows its state, and a debug build keeps the link to the source lines. Step into follows a call, step over runs it, and step out returns to the caller.
- [3.7 Using an integrated debugger: Running and breakpoints](07-using-an-integrated-debugger-running-and-breakpoints.md): run to a place stops once, and a breakpoint stays and stops at every call. Set Next Statement skips code and changes what the program does.
- [3.8 Using an integrated debugger: Watching variables](08-using-an-integrated-debugger-watching-variables.md): a paused program can be inspected, and a watch keeps an expression in view. A watchpoint, or data breakpoint, stops the program when a value changes, after the line that changed it.
- [3.9 Using an integrated debugger: The call stack](09-using-an-integrated-debugger-the-call-stack.md): every active call has a frame, and the call stack lists them with the current function on top. Moving to a caller's frame shows its variables but does not move the program.
- [3.10 Finding issues before they become problems](10-finding-issues-before-they-become-problems.md): the compiler's warnings, static analysis, tests and sanitizers each catch a different kind of mistake before the debugger is needed. Small functions, frequent builds and fixed warnings prevent many bugs.

## Quiz

### Question 1

Name the kind of mistake in each case: syntax error, semantic error that the compiler finds, or logic error.

- (a) A function is called with two arguments, but its definition takes three parameters.
- (b) A statement ends without its semicolon, and the compiler reports an error on the next line.
- (c) A program that should print the sum of two numbers prints their product.

<details>
<summary>Solution</summary>

(a) is a semantic error that the compiler finds: the call is well formed, but it does not match the function that it names. (b) is a syntax error, because the grammar is broken: the compiler reports it where it noticed the problem, which is one line after the mistake. (c) is a logic error: the program is valid and runs, and only someone who knows what it should print can see that it is wrong.

</details>

### Question 2

These six steps of the debugging process are in the wrong order. Put them in the right one.

1. Retest, including the cases that worked before.
2. Repair the code.
3. Understand why the code produces the wrong result.
4. Reproduce the problem.
5. Decide how to fix it.
6. Find the root cause.

<details>
<summary>Solution</summary>

The order is 4, 6, 3, 5, 2, 1: reproduce the problem, find the root cause, understand why the code is wrong, decide how to fix it, repair the code, and retest. Retesting comes last, and it includes the cases that worked before, because a repair can break something else.

</details>

### Question 3

Which debugger move or tool fits each goal? Choose from step into, step over, step out, breakpoint and watchpoint.

- (a) You want to know what `quote(5, 4)` returns, but you trust how it works.
- (b) You are inside a function and want to return to the code that called it.
- (c) A variable holds a wrong value at the end of the program, and you do not know which line wrote it.
- (d) You want the program to stop every time `boxArea` is about to run, wherever it is called from.

<details>
<summary>Solution</summary>

(a) Step over: the whole call runs, and the debugger stops at the next line of the same function, where you can read the result. (b) Step out, which finishes the current function and stops in its caller. (c) A watchpoint, because it stops at every change of the variable and shows the old and the new value, whichever line makes the change. (d) A breakpoint in `boxArea`, which stays in place and stops at every call.

</details>

### Question 4

A program is paused in the function `average`. The call stack lists, from the top to the bottom: `average`, `total`, `main`. In GDB you type `up` once.

(a) Which function is running?

(b) Which function called `average`?

(c) After `up`, whose variables does `print` show, and where does the next `next` take effect?

<details>
<summary>Solution</summary>

(a) `average`, because the top of the stack is the function that is running. (b) `total`, the frame directly below the top. (c) `print` shows the variables of `total`, because `up` moved your view one frame towards `main`. The program is still paused in `average`, so the next `next` steps through `average`: moving to a frame changes only what you look at.

</details>

### Question 5

Write a program with a function `tripCost` that takes a distance and a rate per unit and returns their product. When the function runs, it must print the line `[debug] tripCost called` with `std::cerr`. The `main` function calls it with 40 and 3, stores the result in a variable, and prints `Trip cost: ` and the result with `std::cout`.

<details>
<summary>Solution</summary>

The debug line goes to `std::cerr`, and the result goes to `std::cout`. The result is stored in a variable before it is printed, so that the debug line does not land in the middle of the output line. The console view shows both streams in the order in which the program wrote them: the first line came from `std::cerr`, and the second line came from `std::cout`.

```cpp title="trip-trace.cpp"
{{#include ../../examples/ch03/x-q5-trip-trace.cpp}}
```

```text title="Output"
{{#include ../../examples/ch03/x-q5-trip-trace.out}}
```

</details>

### Question 6

The program below should print the change due when a customer pays 50 for something that costs 37, so the right output is `Change: 13`. Find the bug and fix it.

```cpp title="change-bug.cpp"
{{#include ../../examples/ch03/x-q6-change-bug.cpp}}
```

```text title="Output"
{{#include ../../examples/ch03/x-q6-change-bug.out}}
```

<details>
<summary>Solution</summary>

The function is right. The mistake is in the call: `changeDue(cost, paid)` passes the cost as the amount paid and the amount paid as the cost, so the function computes 37 minus 50. Both arguments are `int`, so the compiler has no reason to object.

Swap the arguments in the call. The root cause is the call, so changing the function to subtract the other way round would hide the symptom and break every other caller.

```cpp title="change-fixed.cpp"
{{#include ../../examples/ch03/x-q6-change-fixed.cpp}}
```

```text title="Output"
{{#include ../../examples/ch03/x-q6-change-fixed.out}}
```

</details>

### Question 7

The program below should print what percentage of the seats are sold. A theater with 120 seats has sold 30, so the right output is `Sold: 25 percent`. Find the bug and fix it.

```cpp title="percent-bug.cpp"
{{#include ../../examples/ch03/x-q7-percent-bug.cpp}}
```

```text title="Output"
{{#include ../../examples/ch03/x-q7-percent-bug.out}}
```

<details>
<summary>Solution</summary>

The expression `part / whole * 100` is evaluated from left to right. The first step is `30 / 120`, a whole-number division, which drops the fraction and gives 0, and 0 times 100 is still 0. Multiply first and divide last, so that the fraction is not lost before it is scaled: `30 * 100` is 3000, and 3000 divided by 120 is 25. A trace of the intermediate values, as lesson 3.4 shows, would have made the 0 visible at once.

```cpp title="percent-fixed.cpp"
{{#include ../../examples/ch03/x-q7-percent-fixed.cpp}}
```

```text title="Output"
{{#include ../../examples/ch03/x-q7-percent-fixed.out}}
```

</details>

### Question 8

Change your program from Question 5 so that the debug line exists only when a macro named `ENABLE_DEBUG` is defined. Define the macro at the top of the file for now. How do you switch the debug output off without editing the file, and what does the program print then?

<details>
<summary>Solution</summary>

The `std::cerr` statement goes between `#ifdef ENABLE_DEBUG` and `#endif`, and the line `#define ENABLE_DEBUG` at the top defines the name. With the define, the console view is the same as in Question 5:

```cpp title="debug-switch.cpp"
{{#include ../../examples/ch03/x-q8-debug-switch.cpp}}
```

```text title="Output"
{{#include ../../examples/ch03/x-q8-debug-switch.out}}
```

To switch the output off without editing the file, remove the `#define` line from the source and define the macro in the build when you need it, with `-DENABLE_DEBUG` for GCC and Clang or `/DENABLE_DEBUG` for Microsoft's compiler. Without the macro, the preprocessor removes the debug statement, and the program prints only `Trip cost: 120`.

</details>
