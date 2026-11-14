# 1.x Chapter 1 summary and quiz

This page recaps the lessons of Chapter 1 and then tests what you remember. The summary names the key terms of each lesson, so use it to find a lesson that you want to read again. The quiz has eight questions that get harder as you go, and the last four are programs for you to write. Try each question before you open its solution, and build and run your own program before you compare it with the one in the book.

## Summary

- [1.1 Statements and the structure of a program](01-statements-and-the-structure-of-a-program.md): a program is a list of statements, most of which end with a semicolon. Statements live in functions, and the program starts in `main`. A syntax error is a broken grammar rule, and the first error in the list is the one to fix first.
- [1.2 Comments](02-comments.md): the compiler ignores comments. A line comment starts with `//`, a block comment sits between `/*` and `*/`, and block comments do not nest. Good comments say why, not what.
- [1.3 Introduction to objects and variables](03-introduction-to-objects-and-variables.md): an object is a piece of memory that holds a value, and a variable is an object with a name. A definition such as `int width;` gives the variable its type and its name.
- [1.4 Variable assignment and initialization](04-variable-assignment-and-initialization.md): initialization gives a variable its first value, and assignment replaces it later. List initialization with braces does not allow narrowing, so the book uses braces and writes `{}` when the real value arrives later.
- [1.5 Introduction to iostream: cout, cin, and endl](05-introduction-to-iostream-cout-cin-and-endl.md): `std::cout` with `<<` prints, and `std::cin` with `>>` reads after the reader presses <kbd>Enter</kbd>. `"\n"` ends a line, `std::endl` also flushes, and a failed read leaves the stream unusable.
- [1.6 Uninitialized variables and undefined behavior](06-uninitialized-variables-and-undefined-behavior.md): a variable without a value holds an indeterminate value, and reading it is undefined behavior. Implementation-defined and unspecified behavior are milder, and the cure is to initialize every variable.
- [1.7 Keywords and naming identifiers](07-keywords-and-naming-identifiers.md): an identifier is a name you choose, and it cannot be a keyword, start with a digit or contain a space. Names with a double underscore or a leading underscore and capital are reserved, and the book uses camelCase.
- [1.8 Whitespace and basic formatting](08-whitespace-and-basic-formatting.md): whitespace separates tokens and is otherwise mostly ignored, except in string literals and `//` comments. Neighboring string literals are joined, and a formatter applies one layout everywhere.
- [1.9 Introduction to literals and operators](09-introduction-to-literals-and-operators.md): a literal is a value written in the code. Operators work on operands and are unary, binary or ternary, whole-number division drops the fraction, and precedence decides what is calculated first.
- [1.10 Introduction to expressions](10-introduction-to-expressions.md): an expression is evaluated to a result and may have a side effect. Expressions contain subexpressions, and an expression statement whose result is thrown away has no effect.
- [1.11 Developing your first program](11-developing-your-first-program.md): write a plan, build one piece at a time, test after each piece, and start with fixed values before you add input.

## Quiz

### Question 1

Look at these five lines:

```cpp
int tickets{12};
tickets = 15;
int refunds = 2;
int pending(4);
int spare{};
```

Which line is an assignment? For each of the other lines, name the form of initialization, and say what the variable holds.

<details>
<summary>Solution</summary>

The second line, `tickets = 15;`, is the assignment: `tickets` already exists, so the line replaces its value of 12 with 15.

The other four lines create variables. `int tickets{12};` is list initialization, and `tickets` starts as 12. `int refunds = 2;` is copy initialization, and `refunds` holds 2. `int pending(4);` is direct initialization, and `pending` holds 4. `int spare{};` is value initialization, and `spare` holds 0.

</details>

### Question 2

What does this fragment print?

```cpp
int a{7};
int b{2};
std::cout << a / b << " " << a - b * 2 << "\n";
```

<details>
<summary>Solution</summary>

It prints `3 3`. Both numbers are whole numbers, so `7 / 2` drops the fraction and gives 3. In `a - b * 2`, the multiplication comes first, `2 * 2` is 4, and `7 - 4` is 3.

</details>

### Question 3

One of these lines is wrong, although the program may appear to work. Which one, and why?

```cpp
int low{1};
int high;
std::cout << low << "\n";
std::cout << high << "\n";
```

<details>
<summary>Solution</summary>

The last line is wrong. The variable `high` is defined without an initializer, so the line reads an indeterminate value, which is undefined behavior. The program may print a number that looks fine today and a different one tomorrow. The fix is to initialize it, for example with `int high{9};`, or with `int high{};` when the real value is not known yet.

</details>

### Question 4

Which of these names are valid identifiers: `seats2`, `2seats`, `seat count`, `_Total`, `Total`, `return`, `bookCount`? Which of the valid ones should you still avoid?

<details>
<summary>Solution</summary>

`2seats` starts with a digit, `seat count` contains a space, and `return` is a keyword, so these three are not valid. The other four are valid names. Of those, `_Total` should be avoided: a name that starts with an underscore and a capital letter is reserved for the compiler and the Standard Library.

</details>

### Question 5

Write a program that defines the number of rows in a theater, 8, and the number of seats in each row, 12. It calculates the total number of seats in a third variable and prints it.

<details>
<summary>Solution</summary>

Define one variable for each of the two numbers, give the third variable the result of the multiplication as its initial value, and print it:

```cpp title="theater-seats.cpp"
{{#include ../../examples/ch01/x-q5-theater-seats.cpp}}
```

```text title="Output"
{{#include ../../examples/ch01/x-q5-theater-seats.out}}
```

</details>

### Question 6

Write a program that asks how many eggs there are, and prints how many full boxes of 12 eggs that makes and how many eggs are left over. Only the operators from lesson 1.9 are allowed.

<details>
<summary>Solution</summary>

Whole-number division gives the full boxes, because it drops the fraction. The eggs that are left are the total minus the eggs that sit in the full boxes. Type 29 and press <kbd>Enter</kbd> to see the result for 29 eggs:

```cpp title="egg-boxes.cpp"
{{#include ../../examples/ch01/x-q6-egg-boxes.cpp}}
```

```text title="Example session"
{{#include ../../examples/ch01/x-q6-egg-boxes.session}}
```

</details>

### Question 7

Write a program that reads three whole numbers and prints their average, rounded down. Take care of the order of the operations.

<details>
<summary>Solution</summary>

The sum has to be calculated before the division, so it needs parentheses. Without them, `first + second + third / 3` would divide only the last number. Type 7, 10 and 14 on one line, separated by spaces, and press <kbd>Enter</kbd>:

```cpp title="average-of-three.cpp"
{{#include ../../examples/ch01/x-q7-average-of-three.cpp}}
```

```text title="Example session"
{{#include ../../examples/ch01/x-q7-average-of-three.session}}
```

The sum is 31, and 31 divided by 3 is 10 with a remainder, so the average that is rounded down is 10.

</details>

### Question 8

Write a program that defines two variables, `left` with the value 3 and `right` with the value 8, and prints them. Then it swaps their values, so that `left` holds 8 and `right` holds 3, and prints them again. You may define one more variable.

<details>
<summary>Solution</summary>

Assigning one variable to the other would lose a value, because an assignment destroys the old value. The extra variable keeps a copy of the first value while the two assignments take place:

```cpp title="swap-values.cpp"
{{#include ../../examples/ch01/x-q8-swap-values.cpp}}
```

```text title="Output"
{{#include ../../examples/ch01/x-q8-swap-values.out}}
```

</details>
