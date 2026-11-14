# 1.4 Variable assignment and initialization

A variable is only useful once it holds a value. C++ gives you two ways to put one there: you can give the variable a value at the moment it is created, or you can replace its value later. This lesson explains the difference between the two, shows the several ways to write the first, and explains why this book prefers one of them.

## Initialization and assignment

Giving a variable a value at the moment it is created is called **initialization**. Replacing the value of a variable that already exists is called **assignment**, and it uses the `=` operator.

```cpp
int score{10};
score = 25;
```

The first line creates `score` and starts it at 10, which is initialization. The second line puts 25 into the existing variable, which is assignment. The old value, 10, is gone.

The equals sign makes the two hard to tell apart, because it also appears in one way of writing an initialization, as you will see in a moment. A good way to separate them is to ask whether the line creates a variable. If it starts with a type, such as `int`, the variable is being created and the line is an initialization. If it only has a name, the variable already exists and the line is an assignment.

## Forms of initialization

C++ has several ways to initialize a variable, and each has a name. The table shows all of them for an `int`.

| Form | Example | What the variable holds |
| --- | --- | --- |
| Default | `int a;` | An indeterminate value |
| Copy | `int b = 5;` | 5 |
| Direct | `int c(6);` | 6 |
| List | `int d{7};` | 7 |
| Value | `int e{};` | 0 |

**Default initialization** is what happens when you write no initializer at all. For an `int` it means that no value is stored, and the variable holds whatever was left in that piece of memory before. Lesson 1.6 explains why that is dangerous.

**Copy initialization** uses an equals sign, and **direct initialization** uses parentheses. Both come from older versions of the language, and you will see them in a lot of existing code.

**List initialization** uses braces, and it arrived with C++11. When the braces are empty, as in `int e{};`, the result is **value initialization**: the variable gets a value that is zero for numbers. This program uses four of the forms, and then assigns a new value to one of the variables:

```cpp title="initialization.cpp"
{{#include ../../examples/ch01/04-initialization.cpp}}
```

It prints:

```text title="Output"
{{#include ../../examples/ch01/04-initialization.out}}
```

## Why this book uses braces

All of the forms with an initial value do the same job for an `int` and a value that fits. The difference shows up when the value does not fit, and that is where list initialization is better. A **narrowing conversion** is a conversion that can change or lose the value, such as turning 4.5 into a whole number. List initialization does not allow narrowing conversions.

```cpp title="narrowing.cpp"
{{#include ../../examples/ch01/04-narrowing.fail.cpp}}
```

The number 4.5 has a fraction, and an `int` cannot hold a fraction. The standard makes a narrowing conversion in a brace initializer ill-formed, so this program is not valid C++. GCC and Clang both refuse to build it with their default settings, with or without the options from lesson 0.11.

The other forms are more relaxed. An initializer such as `int x = 4.5;` is accepted and quietly stores 4, although the strict warnings of lesson 0.11 report it. Writing braces makes the compiler catch the mistake in every case, so the book writes braces for every variable.

> [!BEST-PRACTICE]
> Initialize every variable with braces. Give the variable its real value when you know it, and use empty braces, as in `int total{};`, when the real value will arrive a moment later, for example from the keyboard in the next lesson.

## Assignment is not initialization

It is tempting to think that an assignment is a slower way to initialize, but the two are different operations. Initialization creates a variable with its first value. Assignment destroys the old value and puts a new one in its place.

A variable that is initialized in one step is also simpler to reason about than one that is created first and filled later. Between those two moments the variable has no meaningful value, and every line that could run there is a chance for a mistake.

## Variables that you never use

The options of lesson 0.11 turn an unused variable into an error. This keeps a program free of leftovers, but you sometimes need a variable that the program does not use, for example while you are experimenting. In that case you can mark the variable with the attribute `[[maybe_unused]]`, which has been part of C++ since C++17:

```cpp
[[maybe_unused]] int spare{3};
```

The attribute tells the compiler that the missing use is on purpose. Use it rarely. In most cases the better fix is to delete the variable.

<details>
<summary>Check your understanding</summary>

**Question 1.** Which of these lines is an assignment, and which are initializations?

```cpp
int a{3};
a = 4;
int b = 5;
```

<details>
<summary>Answer</summary>

`a = 4;` is the assignment, because `a` already exists. `int a{3};` and `int b = 5;` are initializations, because each of them creates a variable.

</details>

**Question 2.** What does this fragment print?

```cpp
int x{1};
x = 2;
int y{x};
std::cout << y;
```

<details>
<summary>Answer</summary>

It prints `2`. The assignment changes `x` to 2, and `y` is then created with the current value of `x`.

</details>

**Question 3.** What happens when you build a program that contains `int n{2.5};`?

<details>
<summary>Answer</summary>

The build fails. A brace initializer does not allow a narrowing conversion, and turning 2.5 into an `int` would lose the fraction.

</details>

</details>

## Summary

- Initialization gives a variable its first value when it is created, and assignment replaces the value of an existing variable.
- The forms of initialization are default (`int a;`), copy (`int b = 5;`), direct (`int c(6);`), list (`int d{7};`) and value (`int e{};`).
- List initialization rejects narrowing conversions, such as `int n{4.5};`, so this book initializes with braces.
- Empty braces give a zero, which is a good start when the real value will arrive soon.
- An unused variable is an error under the book's options, and `[[maybe_unused]]` is the way to say that it is on purpose.

## Further reading

- [Initialization (cppreference)](https://en.cppreference.com/w/cpp/language/initialization)
- [List-initialization (cppreference)](https://en.cppreference.com/w/cpp/language/list_initialization)
- [The maybe_unused attribute (cppreference)](https://en.cppreference.com/w/cpp/language/attributes/maybe_unused)
