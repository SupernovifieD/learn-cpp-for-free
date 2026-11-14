# 2.x Chapter 2 summary and quiz

This page recaps the lessons of Chapter 2 and then tests what you remember. The summary names the key terms of each lesson, so use it to find a lesson that you want to read again. The quiz has eight questions, and the last four are programs for you to write, one of them a program of several files. Try each question before you open its solution, and build and run your own program before you compare it with the one in the book.

## Summary

- [2.1 Introduction to functions](01-introduction-to-functions.md): a function is a named group of statements, and a call runs it and returns to the caller. A definition has a return type, a name, a parameter list and a body, and a function cannot be defined inside another function.
- [2.2 Function return values](02-function-return-values.md): a `return` statement hands a value back, and the call is an expression that you can use. A function whose return type is not `void` must return a value on every route, and `main` returns a status code, where 0 or `EXIT_SUCCESS` means success.
- [2.3 Void functions (non-value returning functions)](03-void-functions.md): `void` means that a function returns no value, so its call cannot be used as a value. Return a value when the caller needs an answer, and use `void` when the work is the point.
- [2.4 Introduction to function parameters and arguments](04-introduction-to-function-parameters-and-arguments.md): parameters are in the definition and arguments are in the call, and arguments are passed by value, so the function works with copies. The number of arguments must match, and an unused parameter is an error under the book's options.
- [2.5 Introduction to local scope](05-introduction-to-local-scope.md): a local variable belongs to its function, its scope runs from the definition to the end of the block, and its lifetime is the time that it exists. Equal names in different functions are independent, and a variable should be defined close to its first use.
- [2.6 Why functions are useful, and how to use them effectively](06-why-functions-are-useful-and-how-to-use-them-effectively.md): functions organize a program, allow reuse and testing, and make changes simpler. A function should have one job and a name that starts with a verb.
- [2.7 Forward declarations and definitions](07-forward-declarations-and-definitions.md): the compiler reads a file from top to bottom, so a function must be declared before it is called. A forward declaration is a function's return type, name and parameters followed by a semicolon, and the one-definition rule allows only one definition of each function.
- [2.8 Programs with multiple code files](08-programs-with-multiple-code-files.md): each source file is compiled on its own and the linker joins the results. A file that calls a function from another file needs a declaration, and every source file must be part of the build.
- [2.9 Naming collisions and an introduction to namespaces](09-naming-collisions-and-an-introduction-to-namespaces.md): a naming collision between files is found by the linker. Namespaces keep names apart, `::` selects a name from one, and the book writes `std::` instead of using `using namespace std;`.
- [2.10 Introduction to the preprocessor](10-introduction-to-the-preprocessor.md): the preprocessor handles the `#` lines before the compiler and produces a translation unit. `#define` makes macros, which replace plain text, and `#ifdef`, `#ifndef`, `#if 0` and `#endif` keep or drop code.
- [2.11 Header files](11-header-files.md): a header holds declarations that many files share, and `#include` copies it into a file. Use quotation marks for your own headers and angle brackets for the Standard Library, and include what you use.
- [2.12 Header guards](12-header-guards.md): `#ifndef`, `#define` and `#endif` make a header count once per source file. A guard does not stop two source files from each defining a function, so headers hold declarations.
- [2.13 How to design your first programs](13-how-to-design-your-first-programs.md): state the goal and the requirements, list the tasks in order, and build one task at a time, testing after each one.

## Quiz

### Question 1

What does this program print?

```cpp title="call-order.cpp"
{{#include ../../examples/ch02/x-q1-call-order.cpp}}
```

<details>
<summary>Solution</summary>

```text title="Output"
{{#include ../../examples/ch02/x-q1-call-order.out}}
```

The first call shows 3. The second call evaluates `addOne(start)` first, and shows 4. The third call evaluates the inner call, which gives 4, then `twice(4)`, which gives 8. The last call shows 3 again, because every argument was passed by value, so `start` was never changed.

</details>

### Question 2

The compiler reports an error for these lines. What is wrong?

```cpp
int twice(int number);
void twice(int number)
{
    std::cout << number * 2;
}
```

<details>
<summary>Solution</summary>

The declaration says that `twice` returns an `int`, and the definition says that it returns `void`. A declaration and its definition must agree on the return type, so the compiler rejects the second declaration: the two differ only in their return type. Change one of them to match the other, for example by making the declaration `void twice(int number);`.

</details>

### Question 3

A program has `main.cpp`, which declares `int total(int left, int right);` and calls it, and `total.cpp`, which defines the function. You build it with the command `g++ -std=c++20 -o program main.cpp`. The compiler reports no error, but the build fails. What happened, and how do you fix it?

<details>
<summary>Solution</summary>

The compiler accepted `main.cpp`, because the declaration is enough to check the call. The linker then fails, because it finds no definition of `total`: the command does not name `total.cpp`, so its code is not part of the program. Add the file to the command, as in `g++ -std=c++20 -o program main.cpp total.cpp`.

</details>

### Question 4

Write the include directives for the Standard Library header `<cstdlib>` and for your own header `sizes.h`. Then write the three lines of the header guard for `sizes.h`.

<details>
<summary>Solution</summary>

The directives are `#include <cstdlib>` and `#include "sizes.h"`. Angle brackets are used for the Standard Library and quotation marks for your own files. The guard, written around the content of `sizes.h`, is:

```cpp
#ifndef SIZES_H
#define SIZES_H
#endif
```

The content of the header goes between the `#define` line and the `#endif` line. The name `SIZES_H` is written in capital letters and derived from the name of the file.

</details>

### Question 5

Write a program with a function `average` that takes two whole numbers and returns their average, with the fraction dropped. The `main` function reads two numbers and prints the result.

<details>
<summary>Solution</summary>

The function adds its two parameters and divides the sum by 2. Whole-number division drops the fraction, and the parentheses make the addition happen first. Type 9, a space and 14, and press <kbd>Enter</kbd>:

```cpp title="average-of-two.cpp"
{{#include ../../examples/ch02/x-q5-average-of-two.cpp}}
```

```text title="Example session"
{{#include ../../examples/ch02/x-q5-average-of-two.session}}
```

</details>

### Question 6

Write a program with a `void` function `printScore` that takes the number of a round and the points that were scored in it, and prints a line such as `Round 1: 10 points`. The `main` function calls it three times, with different arguments.

<details>
<summary>Solution</summary>

The function prints and returns nothing, so its return type is `void`. Each call passes two arguments, in the order of the parameters:

```cpp title="print-scores.cpp"
{{#include ../../examples/ch02/x-q6-print-scores.cpp}}
```

```text title="Output"
{{#include ../../examples/ch02/x-q6-print-scores.out}}
```

</details>

### Question 7

Write a program of three files. A header with a header guard declares two functions: `squareArea`, which returns the area of a square, and `squarePerimeter`, which returns its perimeter, each taking the length of a side. A source file defines them, and `main.cpp` reads the side and prints both results.

<details>
<summary>Solution</summary>

The header declares the functions, and it has a guard with the name `SQUARE_H`. The source file includes its own header and defines the functions. The file `main.cpp` includes the header and uses them.

Build the program by naming both source files on the command line, and leave the header out. Type 6 and press <kbd>Enter</kbd>:

```cpp title="square.h"
{{#include ../../examples/ch02/x-q7-square-project/square.h}}
```

```cpp title="square.cpp"
{{#include ../../examples/ch02/x-q7-square-project/square.cpp}}
```

```cpp title="main.cpp"
{{#include ../../examples/ch02/x-q7-square-project/main.cpp}}
```

```text title="Example session"
{{#include ../../examples/ch02/x-q7-square-project.session}}
```

</details>

### Question 8

Write a program that reads a number of minutes and prints it as hours and minutes, for example 135 minutes as 2 hours and 15 minutes. Use two functions, one for the whole hours and one for the minutes that are left over. Use only the arithmetic you have met: whole-number division, multiplication and subtraction.

<details>
<summary>Solution</summary>

The whole hours are the minutes divided by 60, because the division drops the fraction. The minutes that are left are the total minus the minutes that sit in the whole hours, and the second function can use the first. Type 135 and press <kbd>Enter</kbd>:

```cpp title="minutes-to-hours.cpp"
{{#include ../../examples/ch02/x-q8-minutes-to-hours.cpp}}
```

```text title="Example session"
{{#include ../../examples/ch02/x-q8-minutes-to-hours.session}}
```

</details>
