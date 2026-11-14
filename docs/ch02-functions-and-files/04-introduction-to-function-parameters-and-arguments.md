# 2.4 Introduction to function parameters and arguments

A function that always does exactly the same thing is of limited use. The functions you have written so far printed fixed text or asked for input. Most useful functions work on values that their caller gives them: a total on the prices that it is handed, a banner on the text that it is told to show. In this lesson you learn how a caller passes values into a function, and what the function can and cannot do with them.

## Parameters and arguments

A **parameter** is a variable in the parameter list of a function definition. It names the value that the function expects from its caller. An **argument** is the value that a caller supplies in a call. The two words describe the same hand-over from two sides: the definition has parameters, and the call has arguments.

When a function is called, each parameter is initialized with the corresponding argument. The first argument goes into the first parameter, the second into the second, and so on, in order. Inside the function, a parameter is an ordinary variable that already has its value.

This program has a function with two parameters, `tickets` and `pricePerTicket`. It reads two numbers, and it passes them to the function as arguments:

```cpp title="ticket-total.cpp"
{{#include ../../examples/ch02/04-ticket-total.cpp}}
```

Type 3 and press <kbd>Enter</kbd>, then type 12 and press <kbd>Enter</kbd>:

```text title="Example session"
{{#include ../../examples/ch02/04-ticket-total.session}}
```

The call `totalPrice(ticketCount, price)` has two arguments, the values of the variables `ticketCount` and `price`. In the function, `tickets` starts as 3 and `pricePerTicket` starts as 12, and the function returns their product. The names of the arguments in `main` and the names of the parameters in the function do not have to match. What matters is the position.

## Passing by value

The parameters do not share anything with the variables of the caller. When a function is called, each argument is **passed by value**: the value is copied into the parameter. The function works with its own copy, and the variable in the caller stays as it was.

```cpp title="pass-by-value.cpp"
{{#include ../../examples/ch02/04-pass-by-value.cpp}}
```

```text title="Output"
{{#include ../../examples/ch02/04-pass-by-value.out}}
```

The function changes `points` to 60, and prints it. Back in `main`, the variable `score` still holds 50, because `points` was only a copy of its value. Later chapters show other ways of passing an argument, in which a function can change the caller's variable. Passing by value is the default, and it is the safest, because a function cannot change a caller's variable by accident.

## The number of arguments must match

A call must supply exactly as many arguments as the function has parameters. If it does not, the compiler cannot find a function that fits the call:

```cpp title="wrong-argument-count.cpp"
{{#include ../../examples/ch02/04-wrong-argument-count.fail.cpp}}
```

The function `totalPrice` needs two values, and the call gives it one. The compiler reports that there is no matching function for the call, or that the call has too few arguments, depending on the compiler. The same error appears when a call has too many arguments.

## Using a return value as an argument

An argument can be any expression of the right type, and a call to a function is an expression. You can therefore pass the result of one function straight into another:

```cpp title="nested-calls.cpp"
{{#include ../../examples/ch02/04-nested-calls.cpp}}
```

```text title="Output"
{{#include ../../examples/ch02/04-nested-calls.out}}
```

In `twice(addOne(4))`, the inner call runs first. It returns 5, and that value becomes the argument of `twice`, which returns 10. In `addOne(twice(4))` the order of the functions is reversed, so the result is 9.

## The order in which arguments are evaluated

When a call has several arguments, each of them is evaluated before the function runs, but the standard does not say in which order. Consider a call like this one, where `readNumber` is the function from lesson 2.2:

```cpp
int total{totalPrice(readNumber(), readNumber())};
```

The two reads could happen in either order, so the reader's first number could become either `tickets` or `pricePerTicket`. The result can differ from one compiler to the next.

> [!WARNING]
> Do not write a call whose result depends on the order in which its arguments are evaluated. Read each value into its own variable first, in the order that you want, and then pass the variables.

## Parameters that the function does not use

A parameter that a function never uses is probably a mistake, and the options of lesson 0.11 turn it into an error. If a parameter has to be there, for example because callers expect a function of that shape, there are two ways to say that its absence of use is on purpose. You can leave out its name, which is the usual choice:

```cpp
void greet(int)
```

Or you can mark the parameter with the attribute from lesson 1.4, placed directly in front of the parameter:

```cpp
void greet([[maybe_unused]] int times)
```

In most cases, the better fix is to delete a parameter that nothing uses.

<details>
<summary>Check your understanding</summary>

**Question 1.** In the definition `int add(int first, int second)` and the call `add(2, offset)`, which names or values are parameters and which are arguments?

<details>
<summary>Answer</summary>

`first` and `second` are the parameters, because they are in the definition. `2` and `offset` are the arguments, because they are in the call.

</details>

**Question 2.** The program in this lesson calls `addBonus(score)`. What does `score` hold after the call, and why?

<details>
<summary>Answer</summary>

It still holds 50. The argument is passed by value, so `points` is a copy of the value 50. The function changes the copy, and `score` is not touched.

</details>

**Question 3.** The following function fails to build with the book's options. Why?

```cpp
int twice(int number, int spare)
{
    return number * 2;
}
```

<details>
<summary>Answer</summary>

The parameter `spare` is never used, and the options turn the warning about an unused parameter into an error. Remove the parameter, or leave out its name if callers still need to pass a second value.

</details>

</details>

## Summary

- A parameter is a variable in a function definition, and an argument is the value that a call supplies for it.
- Each parameter is initialized with the corresponding argument, by position, and an argument is passed by value, so the function works with a copy.
- A call must have as many arguments as the function has parameters.
- The result of one call can be the argument of another, and the inner call runs first.
- The order in which arguments are evaluated is not specified, so a call should not depend on it.
- An unused parameter is an error under the book's options, and the cure is to remove it, leave out its name or mark it with `[[maybe_unused]]`.

## Further reading

- [Function declaration: parameters (cppreference)](https://en.cppreference.com/w/cpp/language/function)
- [Function-call operator (cppreference)](https://en.cppreference.com/w/cpp/language/operator_other)
- [Order of evaluation (cppreference)](https://en.cppreference.com/w/cpp/language/eval_order)
