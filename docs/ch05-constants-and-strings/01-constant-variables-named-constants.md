# 5.1 Constant variables (named constants)

A program is full of values that never change while it runs: the fee for a campsite pitch, the number of seats in a row, the number of minutes in an hour. Writing each one as a bare number works, until the day a number has to change and you cannot tell which of the forty `25`s in the program to touch. This lesson shows how to give such a value a name, and how to ask the compiler to guard it.

## Literal constants and named constants

A literal, as [lesson 1.9](../ch01-cpp-basics/09-introduction-to-literals-and-operators.md) explained, is a value written directly in the code, such as `25`. Its value cannot change, so it is a **literal constant**. A **named constant** is a constant that has a name, and the name is what makes it useful: it says what the value means and gives you one place to change it.

You create one with the keyword `const`. A variable that is defined with `const` cannot be changed after its definition, and the result is called a **constant variable**. The name sounds contradictory, but the value is fixed and the name is a variable's name, and the book uses it in both senses.

```cpp
const int pitchFee{25};
```

The keyword goes in front of the type, and the rest is an ordinary definition with a brace initializer, as in [lesson 1.4](../ch01-cpp-basics/04-variable-assignment-and-initialization.md).

## Magic numbers

A **magic number** is a literal whose meaning is not clear from the code, or that is repeated in several places. This program prices a stay at a campsite for three nights and two tents:

```cpp title="magic-numbers.cpp"
{{#include ../../examples/ch05/01-magic-numbers.cpp}}
```

```text title="Output"
{{#include ../../examples/ch05/01-magic-numbers.out}}
```

The first `25` is the fee for a pitch, and the second `25` is a deposit. They are the same number by chance.

When the pitch fee goes up to 30, which of the two should change? A reader cannot tell, and a tired programmer will guess. [Lesson 1.11](../ch01-cpp-basics/11-developing-your-first-program.md) mentioned magic numbers, and this program shows why they cause trouble.

A named constant removes the guesswork. Each value gets its own name, and each name says what the number is for:

```cpp title="named-constants.cpp"
{{#include ../../examples/ch05/01-named-constants.cpp}}
```

```text title="Output"
{{#include ../../examples/ch05/01-named-constants.out}}
```

The output is the same, and the program is simpler to read and to change. The pitch fee appears in one place, so raising it means editing one line, and the deposit does not change by accident.

## A constant must have a value, and keeps it

A constant of a fundamental type has to be given its value when it is defined, because there will be no second chance. A definition without a value is an error:

```cpp title="uninitialized.cpp"
{{#include ../../examples/ch05/01-uninitialized.fail.cpp}}
```

The compiler rejects the definition, because a `const` object needs an initial value. The other half of the rule is that the value cannot be replaced later:

```cpp title="assign-to-const.cpp"
{{#include ../../examples/ch05/01-assign-to-const.fail.cpp}}
```

The assignment is an error, and the message names the variable and says that it is read-only or `const`. This is the point of the keyword: if a line tries to change something that you promised to keep, the compiler finds it for you.

The value does not have to be a literal. A constant can be set from a calculation, from a value that is read while the program runs, or from other constants, as in `const int total{nights * pitchFee};`. `const` only means that the value cannot change after the definition. Lessons [5.5](05-constant-expressions.md) and [5.6](06-constexpr-variables.md) return to the question of when the value is known.

## Naming constants

A constant is a variable, so it follows the naming rules of [lesson 1.7](../ch01-cpp-basics/07-keywords-and-naming-identifiers.md): this book writes `pitchFee` in the same camelCase as every other variable, with no prefix. You will see other styles in other code, such as `PITCH_FEE`, and a team may prefer one of them. The best choice is the style that the project already uses, and in this book it is camelCase.

## const and functions

You can write `const` in front of a function's by-value parameter: `void printFee(const int fee)`. The parameter is a copy of the argument, so changing it inside the function could never affect the caller anyway, and the keyword adds little. This book leaves it out of by-value parameters, to keep the signatures short.

A `const` in front of a returned fundamental type has no effect on the value that the caller receives, because the caller receives a copy that it may use as it likes. The compiler even says so:

```cpp title="const-return.cpp"
{{#include ../../examples/ch05/01-const-return.fail.cpp}}
```

The second line of the file says that the program builds without `-Werror`, which means that the compiler only warns, and the book's options turn the warning into an error. Do not write `const` on a returned value of a fundamental type. A later chapter shows where `const` on a parameter really matters, when the parameter is not a copy.

## Prefer const to macros

[Lesson 2.10](../ch02-functions-and-files/10-introduction-to-the-preprocessor.md) showed that the preprocessor can give a name to a value with `#define`. That works, but a named constant is better:

```cpp
#define PITCH_FEE 25
const int pitchFee{25};
```

The macro is replaced by text before the compiler sees the program. It has no type, it ignores scope, and a debugger usually cannot show its name, because the name no longer exists once the preprocessor is done. The constant variable has a type that the compiler checks, a scope, and a name that the debugger shows, as [lesson 3.8](../ch03-debugging/08-using-an-integrated-debugger-watching-variables.md) described for variables.

> [!BEST-PRACTICE]
> Give every value that has a meaning a name, with `const` when it can be set once. Use a plain literal only where the number is obvious, such as 0 and 1, and use a constant instead of an object-like macro.

How to share one constant between several files is a topic for a later chapter, because it needs more of the language than you have met.

<details>
<summary>Check your understanding</summary>

**Question 1.** What is wrong with `const int seats{40}; seats = 45;`?

<details>
<summary>Answer</summary>

The second statement assigns to a variable that is `const`, which is an error. The compiler refuses to build the program, and that is how it protects the value that you promised not to change.

</details>

**Question 2.** Why does `const int fee;` not build, even if the program never uses `fee`?

<details>
<summary>Answer</summary>

A constant cannot be given a value later, so it must have one when it is defined. A definition without a value would leave a constant that nobody could ever set.

</details>

**Question 3.** A program computes `nights * 25` in one place and `guests * 25` in another, where the second 25 is the price of a meal. Why is this a problem, and what is the fix?

<details>
<summary>Answer</summary>

Both literals are magic numbers with the same value but different meanings, so changing the fee for a pitch could change the wrong place. Define two constants with their own names, such as `pitchFee` and `mealPrice`, and use the names.

</details>

</details>

## Summary

- A literal constant is a value in the code, and a named constant gives a value a name that says what it means.
- `const` before the type makes a variable that cannot be changed after its definition.
- A constant of a fundamental type must be initialized when it is defined, and assigning to it is an error.
- A magic number is a literal whose meaning is unclear, and a named constant replaces it.
- The book writes constants in camelCase, does not use `const` on by-value parameters or returned values, and prefers `const` variables to object-like macros.

## Further reading

- [const and volatile qualifiers (cppreference)](https://en.cppreference.com/w/cpp/language/cv)
- [The C++ Core Guidelines: Constants and immutability](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-const)
