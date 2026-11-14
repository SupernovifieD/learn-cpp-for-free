# 2.7 Forward declarations and definitions

The functions you have written so far all came before `main`, and there was a reason for that. In this lesson you find out what happens when a function comes after the place where it is called, and you learn the tool that lets you put your functions in any order: the forward declaration. Along the way you will see the difference between declaring and defining a function, and the rule that every function has exactly one definition.

## The compiler reads from top to bottom

The compiler reads a source file from the first line to the last, and it learns about names as it goes. When it reaches a call to a function, it must already know that the function exists. This program calls `add` before the line where `add` is defined:

```cpp title="call-before-definition.cpp"
{{#include ../../examples/ch02/07-call-before-definition.fail.cpp}}
```

The compiler refuses to build it. When it reads the call in `main`, it has not yet seen any function called `add`, so it reports that the name is not declared. It does not look ahead to find a definition further down. The definition is there, but it is too late.

The simplest cure is to reorder the file. If you move the definition of `add` above `main`, the compiler has seen the function before the call, and the program builds. For a small program, this is all that you need.

## Forward declarations

Reordering does not always work. In a larger program, you may want `main` at the top of the file, where a reader looks first, with the details below it. Two functions can also call each other, and then neither one can come first. For these cases, C++ lets you tell the compiler about a function before you define it.

A **forward declaration**, also called a **function prototype**, is the header of a function followed by a semicolon, with no body. It states the return type, the name and the parameters, which is everything that the compiler needs in order to check a call:

```cpp title="forward-declaration.cpp"
{{#include ../../examples/ch02/07-forward-declaration.cpp}}
```

```text title="Output"
{{#include ../../examples/ch02/07-forward-declaration.out}}
```

The line `int add(int left, int right);` is the forward declaration. When the compiler reaches the call in `main`, it already knows that `add` takes two whole numbers and returns a whole number, so it accepts the call. The definition can follow later in the file, and it must match the declaration.

## Declarations and definitions

Lesson 0.5 introduced the two words that this lesson has been using. A declaration tells the compiler that a function exists and how to call it. A definition supplies the body, the statements that run. The forward declaration of `add` is a declaration, and the function with the braces is the definition.

A declaration is enough for the compiler, but it is not enough for the finished program. If the program calls a function that is declared and never defined, the compiler accepts the program and the linker then fails:

```cpp title="missing-definition.cpp"
{{#include ../../examples/ch00/05-missing-definition.fail.cpp}}
```

This is the program from lesson 0.5. The compiler is satisfied by the declaration of `greet`, but the linker cannot find any code to run for it. The two errors come from two different tools, and lesson 0.5 describes how to tell them apart.

## The one-definition rule

A function may be declared as many times as you like, but it may be defined only once. This rule is called the **one-definition rule**, and in its simplest form it says that a program may contain only one definition of each function. If a file contains two definitions of the same function, the compiler reports an error:

```cpp title="duplicate-definition.cpp"
{{#include ../../examples/ch02/07-duplicate-definition.fail.cpp}}
```

The second definition of `add` is a redefinition, and the compiler rejects it, even though the second body does the same work. The rule also applies to a program of several files: two files that both define the same function cause an error when the program is linked. Lesson 2.9 shows that case.

## Names in declarations

The parameter names in a forward declaration are optional, because the compiler only needs their types in order to check a call. These two declarations mean the same thing:

```cpp
int add(int left, int right);
int add(int, int);
```

> [!BEST-PRACTICE]
> Keep the parameter names in a declaration. They document what each value is for, and a reader who only sees the declaration, as in a header file that you will meet in lesson 2.11, relies on them.

<details>
<summary>Check your understanding</summary>

**Question 1.** Which of these lines is a forward declaration, and which is a definition?

```cpp
int twice(int number);
int twice(int number)
{
    return number * 2;
}
```

<details>
<summary>Answer</summary>

The first line is a forward declaration, because it ends with a semicolon and has no body. The function after it is a definition, because it has a body in braces.

</details>

**Question 2.** What happens when you build a program in which `main` calls a function `twice` that is declared above `main` but defined nowhere?

<details>
<summary>Answer</summary>

The compiler accepts the program, because the declaration is enough to check the call. The linker then fails, because it finds no definition of `twice`.

</details>

**Question 3.** Why does the compiler reject a file that defines the same function twice, even when both definitions are identical?

<details>
<summary>Answer</summary>

The one-definition rule allows only one definition of each function in a program, so the second definition is an error, whatever its body is.

</details>

</details>

## Summary

- The compiler reads a file from top to bottom, so a function must be declared or defined before its first call.
- A forward declaration, or function prototype, is a function header followed by a semicolon, and it lets you call a function that is defined further down or in another file.
- A declaration tells the compiler how to call a function, and a definition supplies the body.
- A function that is declared and called but never defined compiles, and then fails to link.
- The one-definition rule allows a function to be declared many times but defined only once.
- Parameter names are optional in a declaration, but it is good practice to keep them.

## Further reading

- [Definitions and the one-definition rule (cppreference)](https://en.cppreference.com/w/cpp/language/definition)
- [Function declaration (cppreference)](https://en.cppreference.com/w/cpp/language/function)
