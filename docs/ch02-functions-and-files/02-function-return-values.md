# 2.2 Function return values

The functions in the last lesson did something and then returned nothing. Many functions are different: you ask them a question or ask them to calculate, and they give you an answer. In this lesson you learn how a function hands a value back to its caller, how to use that value, and what the compiler says when a function forgets to return one.

## Returning a value

The return type in front of a function's name says what kind of value the function gives back. When the return type is `int`, the function hands back a whole number. The statement that does the handing is the return statement, `return`, followed by the value:

```cpp title="read-number-twice.cpp"
{{#include ../../examples/ch02/02-read-number-twice.cpp}}
```

The function `readNumber` asks a question, reads a number into its own variable `value`, and returns that number. In `main`, the call `readNumber()` is an expression, as lesson 1.10 described, and its result is whatever the function returned. That result initializes `first`, and a second call initializes `second`. Type 4 and press <kbd>Enter</kbd>, then type 9 and press <kbd>Enter</kbd>:

```text title="Example session"
{{#include ../../examples/ch02/02-read-number-twice.session}}
```

The question appears twice, because the function runs again for each call, and each call returns the number that the reader typed for it. This is the reuse that lesson 2.1 promised: the three statements that ask for a number are written once.

A `return` statement also ends the function at once. The computer leaves the function at the `return`, and the statements after it never run. That is why a return statement usually comes last.

## Using the returned value

A call is an expression, so you can use it wherever you can use a value of its type. You can store the result in a variable, as the program above does, or you can use it as an operand:

```cpp
int doubled{readNumber() * 2};
```

Here the function is called first, and its result is multiplied by 2. A call can also stand alone as a statement, as in `readNumber();`, but then the result is thrown away. Unlike the statement `width * 2;` in lesson 1.10, this is not an error, because the call has a useful side effect: it reads a number. Still, a function that returns a value is usually called because the caller wants the value.

A function can return only one value. Later chapters show other ways to get several results out of a function.

## Every path must return a value

When a function has a return type other than `void`, the caller expects a value to come back. If the function runs to its closing brace without reaching a `return`, no value comes back:

```cpp title="missing-return.cpp"
{{#include ../../examples/ch02/02-missing-return.fail.cpp}}
```

The function `getFive` prints a message and then ends without returning anything. The standard says that flowing off the end of a function that returns a value, other than `main`, is undefined behavior, as lesson 1.6 described. The program that uses the result could print any number or do anything else.

Both GCC and Clang warn about this mistake, and the options of lesson 0.11 turn the warning into an error, so the program above does not build. Without `-Werror` it builds with the warning, and its behavior is undefined.

In a function this short, you can see the mistake. In a longer function, the problem can hide in one of several routes through the function, and you will need to check that every route ends in a `return`. A later chapter introduces the statements that create such routes.

> [!WARNING]
> A function with a return type other than `void` must return a value on every route through it. Treat the warning about a missing return as a bug, and never switch it off.

## The value that main returns

The function `main` returns an `int` too, and its value goes to the operating system when the program ends. This value is the **status code** of the program. A program that finished its work returns 0, and a program that failed returns another number, so that scripts and other programs can tell what happened.

The names `EXIT_SUCCESS` and `EXIT_FAILURE`, from the header `<cstdlib>`, give a readable name to the two cases. Both 0 and `EXIT_SUCCESS` mean success:

```cpp title="exit-success.cpp"
{{#include ../../examples/ch02/02-exit-success.cpp}}
```

```text title="Output"
{{#include ../../examples/ch02/02-exit-success.out}}
```

A program that has to report a failure ends with the other name:

```cpp
return EXIT_FAILURE;
```

The status code is not printed. Programs and scripts that start your program can read it, and a shell can show it, for example with `echo $?` on Linux and macOS.

The function `main` has one special rule: it may leave out the `return` statement. When the program reaches the end of `main`, the effect is the same as executing `return 0;`. This is allowed only for `main`, and the book still writes the return statement in every program, because it makes the intention clear and because every other function needs one.

<details>
<summary>Check your understanding</summary>

**Question 1.** What does this statement print when the reader types 5 and presses <kbd>Enter</kbd>?

```cpp
std::cout << readNumber() * 2 << "\n";
```

Assume that this is a statement in `main`, and that `readNumber` is the function from this lesson.

<details>
<summary>Answer</summary>

It prints the question `Enter a number: `, and after the reader types 5 it prints `10` and ends the line. The call is evaluated first, its result 5 is multiplied by 2, and the product is inserted into the output.

</details>

**Question 2.** Why is it a mistake for a function that returns an `int` to end without a `return` statement?

<details>
<summary>Answer</summary>

The caller expects a value, and none comes back. The behavior is undefined, so the program may print a surprising number or do anything else. The compilers warn about it, and the book's options turn the warning into an error.

</details>

**Question 3.** What does `main` return if you leave out its `return` statement?

<details>
<summary>Answer</summary>

It returns 0, as if the last statement of `main` were `return 0;`. This is a special rule for `main`, and it does not apply to any other function.

</details>

</details>

## Summary

- A function returns a value with a `return` statement, and the value has the type that the function declares before its name.
- A call is an expression, so its result can initialize a variable or take part in a calculation.
- A `return` statement ends the function at once, and a function returns only one value.
- A function that returns a value must return one on every route through it, because reaching the end without a `return` is undefined behavior, and the compilers warn about it.
- `main` returns a status code, `EXIT_SUCCESS` or 0 for success and `EXIT_FAILURE` for failure, and `main` alone may leave out the `return` statement.

## Further reading

- [The return statement (cppreference)](https://en.cppreference.com/w/cpp/language/return)
- [The main function (cppreference)](https://en.cppreference.com/w/cpp/language/main_function)
- [EXIT_SUCCESS and EXIT_FAILURE (cppreference)](https://en.cppreference.com/w/cpp/utility/program/EXIT_status)
