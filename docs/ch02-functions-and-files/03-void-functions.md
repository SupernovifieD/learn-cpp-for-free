# 2.3 Void functions (non-value returning functions)

Not every function has an answer to give. A function that prints a banner, or that draws something, has done its job when it ends, and there is nothing for the caller to receive. C++ has a return type for exactly this case. In this lesson you learn how a function that returns nothing is written and used, and how to decide between returning a value and returning nothing.

## The void return type

You have already written functions like this in lesson 2.1. The return type `void` means that the function returns no value:

```cpp title="print-banner.cpp"
{{#include ../../examples/ch02/03-print-banner.cpp}}
```

```text title="Output"
{{#include ../../examples/ch02/03-print-banner.out}}
```

The function `printBanner` prints three lines, and it is called twice, once before and once after a line of ordinary output. The function is written once, and the banner is the same both times.

A function that returns `void` does not need a `return` statement. It ends when the computer reaches its closing brace, and the caller continues with the statement after the call. You can also end it with a `return` statement that has no value:

```cpp
void printWelcome()
{
    std::cout << "Welcome\n";
    return;
}
```

A bare `return;` ends the function at that point. At the end of the function it does nothing that the closing brace would not do, so you will rarely write it there. It becomes useful when a function should stop early, which you can arrange once you know statements that make choices.

## A void call is not a value

A call to a function that returns an `int` is an expression with a value, and you can use it wherever a number is allowed. A call to a `void` function is also an expression, but it has no value. It is only a call, and it can only stand alone as a statement.

```cpp title="void-as-value.cpp"
{{#include ../../examples/ch02/03-void-as-value.fail.cpp}}
```

This program tries to use the call `printBanner()` as the initial value of an `int`. The compiler refuses to build it. It reports that it cannot initialize an `int` with a value of type `void`, because the call does not produce a value that could be stored. A similar error appears when you try to insert a `void` call into `std::cout`, or to use it as an operand of an operator.

## Returning a value or returning nothing

When you write a function, you decide how its result reaches the caller. A simple rule helps with the decision. If the caller needs an answer, return it. If the work itself is the point, as in printing, use `void`.

A function that calculates should usually return its result and leave the printing to the caller. Consider two ways of writing a function that works out the total of a bill. One of them prints the total, and the other returns it. The function that prints can only ever print. The function that returns can be printed, stored, compared or used in a further calculation, so it can be reused in many more places.

> [!BEST-PRACTICE]
> Let a function do one job. A function that calculates a result returns it, and a function that shows something prints it. When a function does both, it is harder to reuse and harder to test.

<details>
<summary>Check your understanding</summary>

**Question 1.** Which of these two functions should return `void`: `printReceipt` or `getTotal`?

<details>
<summary>Answer</summary>

`printReceipt` should return `void`, because its job is to print, and the caller needs no value. `getTotal` should return a value, because the caller wants the total for later use.

</details>

**Question 2.** The compiler reports an error for the following line. What is wrong?

```cpp
int banner{printBanner()};
```

<details>
<summary>Answer</summary>

`printBanner` returns `void`, so the call produces no value. There is nothing to store in the variable, and the compiler refuses to build the program.

</details>

</details>

## Summary

- A function with the return type `void` returns no value, and it ends at its closing brace or at a `return;` statement.
- A call to a `void` function can only be used as a statement, never as a value.
- Return a value when the caller needs an answer, and use `void` when the work itself is the point.
- A function that calculates should return its result and leave the printing to its caller.

## Further reading

- [Function declaration: return type void (cppreference)](https://en.cppreference.com/w/cpp/language/function)
