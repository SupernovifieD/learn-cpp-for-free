# 4.2 Void

Every type so far describes values: numbers, characters, yes-or-no answers. One fundamental type describes the absence of a value, and you have already used it without much ceremony. This lesson explains what `void` means, where the language allows it, and where it does not.

## No value, no type of value

The keyword `void` stands for "nothing". Other types describe a set of values that an object can hold, and `void` has no values at all. That is why you cannot make an object out of it, and it is also why it is useful: it lets the language say "nothing" in places where a type is required.

Its most common job is the return type of a function. [Lesson 2.3](../ch02-functions-and-files/03-void-functions.md) introduced functions that do their work and give nothing back:

```cpp
void printBanner()
{
    std::cout << "*** Welcome ***\n";
}
```

The `void` in front of the name tells the compiler and every reader that a call to `printBanner` does not produce a value. The call can stand alone as a statement, and it cannot be used as a value, which is the mistake that lesson 2.3 showed.

## A variable cannot be void

An object is a piece of memory that holds a value, as [lesson 1.3](../ch01-cpp-basics/03-introduction-to-objects-and-variables.md) explained. A type that has no values has nothing to put in that memory, so the compiler cannot decide how much to set aside. The definition is an error:

```cpp title="void-variable.cpp"
{{#include ../../examples/ch04/02-void-variable.fail.cpp}}
```

The compiler refuses to build this program. GCC reports that the variable is declared `void`, and Clang reports that the variable has an incomplete type `void`. Both messages mean the same thing: there is no such thing as a `void` object.

> [!NOTE]
> The first line of the program is a comment that the book's own checks use. It states why the program must fail to build. The page [Conventions used in this book](../conventions.md) explains it.

## An empty parameter list

A function that takes nothing has an empty pair of parentheses, as in `int readValue()`. You may also see `int readValue(void)`, with the word `void` between the parentheses. In C++ the two declare exactly the same function.

The second form is a habit from the C language. In C, an empty pair of parentheses used to mean "the parameters are not described", and the word `void` was the only way to say "no parameters". In C++ the empty parentheses mean no parameters, so the word is not needed.

The C language itself changed in 2023 (C23) and now treats the two forms alike. This book writes the empty pair, and you will see `(void)` only in code that was written for C or that has to work in both languages.

## Void and pointers

`void` has one more role that you will meet much later. A pointer, which is an object that holds the address of another object, can be declared as a pointer to `void` when the type of the object it points to is not known. Pointers have a chapter of their own, so for now it is enough to know that the word `void` shows up there too and that it still means "no particular type".

## What to remember

Use `void` as a return type for a function that does its work and returns nothing, and write an empty pair of parentheses for a function without parameters. Do not try to define a variable of type `void`: the compiler will tell you, and the fix is always to pick the real type of the value that you wanted to store.

<details>
<summary>Check your understanding</summary>

**Question 1.** One of these lines is an error. Which one, and why?

```cpp
void tidyDesk();
void remaining{3};
```

<details>
<summary>Answer</summary>

The second line is the error. `void remaining{3};` defines a variable of type `void`, which has no values. The first line is a valid declaration of a function whose return type is `void`.

</details>

**Question 2.** Are `int rollDie()` and `int rollDie(void)` different functions in C++?

<details>
<summary>Answer</summary>

No, they declare the same function. The `(void)` is a habit from C, and in C++ the empty pair of parentheses is the usual way to write a function without parameters.

</details>

</details>

## Summary

- `void` stands for "no value", and the type has no values at all.
- A function that returns `void` gives nothing back, and a call to it cannot be used as a value.
- A variable cannot have the type `void`, because there is nothing to store.
- In C++, `int f()` and `int f(void)` are the same, and the book writes the empty parentheses.
- `void` also appears in the name of a pointer type, which a later chapter explains.

## Further reading

- [Function declarations: parameter lists (cppreference)](https://en.cppreference.com/w/cpp/language/function)
- [Function declarations in C (cppreference)](https://en.cppreference.com/w/c/language/function_declaration)
- [Fundamental types: void (cppreference)](https://en.cppreference.com/w/cpp/language/types)
