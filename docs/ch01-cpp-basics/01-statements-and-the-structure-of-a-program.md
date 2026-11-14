# 1.1 Statements and the structure of a program

In lesson 0.7 you built a program and ran it without understanding most of its lines. This lesson keeps the promise made there: it takes the program apart and explains what each line is for. Along the way you will meet the two ideas that every C++ program is built from, statements and functions, and you will see what the compiler says when you get the grammar wrong.

## Statements

A **statement** is the smallest complete instruction in a C++ program. You can think of a program as a recipe. The recipe is a list of steps, and each step is a statement that tells the computer to do one thing.

Most statements end with a semicolon, the way most sentences end with a period. The semicolon tells the compiler that the instruction is finished and that the next one may begin.

C++ has several kinds of statements, and you will learn them one at a time. Three of them appear in the next few lessons. An **expression statement** does some work, such as printing text. A **return statement** ends the function that it is in. A **declaration statement** creates a variable, which lesson 1.3 explains. Statements such as `if` and the loops, which make a program choose or repeat, wait until later chapters.

## Functions

A **function** is a named group of statements that run one after another, from the first to the last. Writing statements inside a function is how you give a name to a piece of work. You will write your own functions in Chapter 2. For now it is enough to know that every function has a name and a body, and that the body is the list of statements between a pair of braces, `{` and `}`.

Every C++ program has exactly one function named `main`. When you run the program, the computer starts by running the statements of `main`, from the top. When `main` reaches its end, the program is over.

That makes `main` something like the front door of a building. A building can have many rooms, which are the other functions that you will write, but everybody enters through the door, and the door is always in the same place.

## A tour of the first program

Here is the program from lesson 0.7 again.

```cpp title="hello-world.cpp"
{{#include ../../examples/ch00/07-hello-world.cpp}}
```

Take it one line at a time:

- `#include <iostream>` is not a statement. It is a **preprocessor directive**, an instruction that is handled before the compiler reads the rest of the file. This one asks for the part of the Standard Library that prints text and reads input. Lesson 2.10 explains directives, and lesson 2.11 explains what `#include` does.
- `int main()` starts the definition of the function `main`. The word `int` says that the function hands back a whole number when it ends, and the empty parentheses say that `main` needs nothing from outside to do its work.
- The braces mark where the body of `main` begins and ends.
- `std::cout << "Hello, world!\n";` is an expression statement. It sends the text between the quotation marks to the screen, and `\n` ends the line. Lesson 1.5 explains how this line works.
- `return 0;` is a return statement. It ends `main` and hands the number 0 to the operating system, which reads it as "everything went well". Lesson 2.2 explains return values in detail.

Notice that the line `int main()` has no semicolon. It is the beginning of a function definition, and the statements that belong to it follow in braces. A semicolon belongs at the end of each statement inside the body, not after the closing brace.

## Syntax and syntax errors

Every language has rules for how its pieces fit together. In C++ these rules are called the **syntax** of the language. The compiler checks your code against them, and when something breaks a rule, it stops and reports a **syntax error**.

A missing semicolon is the most common syntax error of all. This program forgets the semicolon after `return 0`:

```cpp title="missing-semicolon.cpp"
{{#include ../../examples/ch01/01-missing-semicolon.fail.cpp}}
```

The compiler refuses to build it. The report says that it expected a semicolon, and it names a file, a line and a column, in the same way that a spell checker underlines the place where it noticed a mistake.

Look at what that location really means. A compiler can only tell that a semicolon is missing when it reaches the next token and finds that the statement does not end where it should. For this program, GCC and Clang both point at the end of the `return 0` line, but a compiler may also point at the beginning of the line after the missing semicolon, depending on the code. If the reported line looks fine, check the line before it.

> [!BEST-PRACTICE]
> Fix the first error in the list, then build again. Later errors are often only side effects of the first one: a single missing semicolon can make the compiler misread everything after it, and the whole list can disappear when you fix that one line.

Lesson 0.8 lists other common problems, and it explains what to do when a build fails.

## Two things the compiler ignores

You can add notes for human readers anywhere in a program, and the compiler skips them. These notes are called comments, and lesson 1.2 shows how to write them. The compiler also pays little attention to spaces and line breaks, and lesson 1.8 explains where they matter and how to use them to make code easy to read.

<details>
<summary>Check your understanding</summary>

**Question 1.** What is wrong with the following lines, and how do you fix it?

```cpp
std::cout << "Good morning\n"
return 0;
```

<details>
<summary>Answer</summary>

The first line is a statement that does not end with a semicolon. Adding `;` after `"Good morning\n"` fixes it. The compiler may report the problem on the first line or on the `return` line, because it notices the problem only when it reaches the next token.

</details>

**Question 2.** Which line of the first program is not a statement, and what is it instead?

<details>
<summary>Answer</summary>

`#include <iostream>` is not a statement. It is a preprocessor directive that tells the preprocessor to make the input and output tools available before the compiler reads the program.

</details>

**Question 3.** How many functions named `main` can a program have, and what does the computer do with it?

<details>
<summary>Answer</summary>

Exactly one. The program starts by running the statements of `main`, and it ends when `main` ends.

</details>

</details>

## Summary

- A statement is the smallest complete instruction in a program, and most statements end with a semicolon.
- Declaration, expression and return statements are three of the kinds you will use first.
- A function is a named group of statements, and every program has exactly one function named `main`, where it starts.
- `#include <iostream>` is a preprocessor directive, not a statement, and `return 0;` hands 0 to the operating system.
- Breaking the syntax rules causes a syntax error, and the reported location can be the line after the real mistake.
- Fix the first error first, and build again before you look at the rest.

## Further reading

- [Statements (cppreference)](https://en.cppreference.com/w/cpp/language/statements)
- [The main function (cppreference)](https://en.cppreference.com/w/cpp/language/main_function)
