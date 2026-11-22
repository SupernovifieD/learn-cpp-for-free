# 5.6 Constexpr variables

A `const` variable promises that a value will not change. It does not promise when the value is known, as [lesson 5.5](05-constant-expressions.md) showed: a `const` variable may be set from input and still be a run-time value. Sometimes you want the other promise, that a value is known while the program is built. C++ has a keyword for it, `constexpr`, and this lesson shows how to use it and when to choose it over `const`.

## The constexpr keyword

A variable that is defined with `constexpr` has to be initialized with a constant expression, and the compiler checks it. If the initializer is not a constant expression, the program does not build. A `constexpr` variable is also `const`, so it cannot change, and you do not need to write both words.

This program describes a small hall. Three of its values are known when the program is built, and one depends on what the reader types. Type 47 and press Enter:

```cpp title="seats.cpp"
{{#include ../../examples/ch05/06-seats.cpp}}
```

```text title="Example session"
{{#include ../../examples/ch05/06-seats.session}}
```

The values `seatsPerRow` and `rows` are literals, and `totalSeats` is calculated from them, so all three are constant expressions and the program defines them with `constexpr`. The value `seatsLeft` depends on the number that was typed, so it cannot be known at build time. It is still a value that never changes after it is set, so the program defines it with `const`. The names use the same camelCase as every other variable.

## When the initializer is not constant

The compiler enforces the keyword. This program tries to make a `constexpr` variable out of a value that was read from the keyboard:

```cpp title="constexpr-input.cpp"
{{#include ../../examples/ch05/06-constexpr-input.fail.cpp}}
```

The build fails, and the message says that `limit` must be initialized by a constant expression. This is the check that you want: a `constexpr` variable is a promise that is verified when you build the program, and not a hope.

## const or constexpr

The two keywords answer different questions, and the choice follows from when the value is known.

| The value | Use |
| --- | --- |
| is known when the program is built | `constexpr` |
| is set while the program runs | `const` |
| must change later | neither |

> [!BEST-PRACTICE]
> Use `constexpr` for every constant whose value is known when the program is built, and `const` for a value that is calculated while the program runs. A `constexpr` variable can be used where the language needs a constant expression, and the compiler proves that it is one.

A `constexpr` variable can be initialized from other `constexpr` variables, as `totalSeats` was, so a chain of constants stays a chain of compile-time values. Beginners sometimes ask whether `constexpr` makes a program faster. It can, because the compiler may use the value directly, but the main gain is the check and the clarity.

The keyword also fixes the problem of floating point constants from lesson 5.5. A `constexpr double` is usable in a constant expression, where a `const double` was not, so the program with `constexpr double width{8.0};` in place of the `const` version builds without a problem.

## Why not use const everywhere

A `const` variable would often do the same job, so why does the language have both? There are four reasons to prefer `constexpr` when you can:

- It tells the reader that the value never depends on input or on a call, so nothing has to be traced to find where the value comes from.
- The compiler checks the claim. A change that makes the value depend on something at run time becomes an error, and not a silent change of meaning.
- It works for every type that can be `constexpr`, while a `const` variable counts as a constant expression only for integers.
- A value that the compiler knows can be folded into the code, as lesson 5.4 described, so that it costs nothing at run time.

## Which types can be constexpr

The fundamental types can all be `constexpr`: integers, floating point numbers, `bool` and `char`. So can `std::string_view`, which lesson 5.8 introduces.

The type `std::string` cannot, at least not in practice. It manages memory that it allocates while the program runs, and C++20 allows that only inside a calculation that frees the memory again before it ends, so a variable cannot hold one. The page for `std::basic_string` on cppreference says that defining a `constexpr` string variable is generally an error, and the compilers that this book is checked with reject it.

## Parameters cannot be constexpr

A function runs with whatever arguments its callers pass, and it exists once, so its parameters get their values at run time. The language therefore does not allow `constexpr` on a parameter:

```cpp title="constexpr-parameter.cpp"
{{#include ../../examples/ch05/06-constexpr-parameter.fail.cpp}}
```

Both compilers reject the parameter. A function that has to be evaluated at compile time is a separate feature, and a later chapter introduces it.

> [!ADVANCED]
> C++20 has two more keywords in this family. A function declared `consteval` must be evaluated at compile time, and a variable declared `constinit` must be initialized at compile time but may change later. The book does not use them.

<details>
<summary>Check your understanding</summary>

**Question 1.** Which line does not build?

```cpp
int n{3};
constexpr int a{n + 1};
```

<details>
<summary>Answer</summary>

The second line. The variable `n` is not `const`, so `n + 1` is not a constant expression, and a `constexpr` variable needs one. Changing `n` to `constexpr` would make both lines build.

</details>

**Question 2.** Choose `const` or `constexpr` for each: the seats per row, always 12; the number of guests that the reader types; the product of rows and seats per row, both of them constants.

<details>
<summary>Answer</summary>

The seats per row is `constexpr`, because the value is a literal. The number of guests is `const` if it must not change after it is read, because it is set at run time. The product is `constexpr`, because it is calculated from constant expressions.

</details>

**Question 3.** Why can a parameter not be `constexpr`?

<details>
<summary>Answer</summary>

A parameter gets its value from the caller while the program runs, and the same function can be called with many different values, so the value is never fixed at build time.

</details>

</details>

## Summary

- `constexpr` defines a variable whose initializer must be a constant expression, and the compiler checks it.
- A `constexpr` variable is also `const`, so it cannot change.
- Use `constexpr` for values known when the program is built, and `const` for values that are set while it runs.
- Fundamental types and `std::string_view` can be `constexpr`, and `std::string` cannot in practice.
- A function parameter cannot be `constexpr`, and `consteval` and `constinit` are related keywords that the book does not use.

## Further reading

- [constexpr specifier (cppreference)](https://en.cppreference.com/w/cpp/language/constexpr)
- [consteval specifier (cppreference)](https://en.cppreference.com/w/cpp/language/consteval)
- [constinit specifier (cppreference)](https://en.cppreference.com/w/cpp/language/constinit)
