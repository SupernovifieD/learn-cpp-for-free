# 5.2 Literals

You have written literals since the first lesson: `42`, `"Hello"`, `3.5`. This lesson looks at them more closely, because every literal has a type, and the compiler chooses that type from the way the literal is spelled. The choice decides how the literal behaves in a calculation, which is why a small difference such as `7 / 2` against `7.0 / 2` changes an answer.

## Every literal has a type

The compiler does not look at the variable that will receive a literal. It looks at the literal itself: its digits, its decimal point, its quotes and its ending. The table shows the types of the literals that this book uses.

| Literal | Type |
| --- | --- |
| `42` | `int` |
| `42u` | `unsigned int` |
| `42LL` | `long long` |
| `42ULL` | `unsigned long long` |
| `3.5` | `double` |
| `3.5f` | `float` |
| `'a'` | `char` |
| `"abc"` | `const char[4]` |
| `true` | `bool` |

The letters at the end of a number are **suffixes**. For whole numbers, `u` means unsigned, `L` means long, and `LL` means long long, and they combine as `UL` and `ULL`. For numbers with a fractional part, `f` means `float`, and an `L` means `long double`, which the book only names. The book writes `L`, `LL`, `UL` and `ULL` in capital letters, because a lowercase `l` looks like the digit 1, and it writes `u` and `f` in lower case.

> [!ADVANCED]
> C++23 added the suffix `uz`, which gives a literal the type `std::size_t`. The book uses C++20, where this suffix does not exist, so you will not see it here.

A whole number without a suffix is an `int` if its value fits. A bigger value gets the first of `long` and `long long` that can hold it, and which one that is depends on the platform. That is why a suffix is the only way to be sure of the type of a large literal.

## The sizes of literals

You can see the size of each type with the `sizeof` operator from [lesson 4.3](../ch04-fundamental-data-types/03-object-sizes-and-the-sizeof-operator.md), which accepts a literal as well. The program leaves out `5L`, because a `long` has different sizes on different platforms:

```cpp title="literal-sizes.cpp"
{{#include ../../examples/ch05/02-literal-sizes.cpp}}
```

```text title="Output"
{{#include ../../examples/ch05/02-literal-sizes.out}}
```

The sizes are the ones on the mainstream platforms that the book targets, and only the size of `char` is fixed by the language.

The surprise is the string literal. `"hello"` has five letters, but its size is 6, because the compiler adds a character with the code 0 at the end, the **null terminator**. A literal like this is a **C-style string**, an array of characters that ends in a null, and it is why the type in the table is `const char[4]` for three letters. [Lesson 5.7](07-introduction-to-std-string.md) introduces `std::string`, which is the better tool for text.

## The type decides the behavior

The type of a literal decides how it prints, too. The character literal `'a'` has the type `char`, so `std::cout` prints a letter, while `97` is an `int` and prints as a number, although both have the same code in ASCII. A `true` is a `bool`, and it prints as 1 unless the stream is switched to words, as [lesson 4.9](../ch04-fundamental-data-types/09-boolean-values.md) showed.

The type also decides how a calculation behaves. Because the literal has its type before it is stored anywhere, the variable on the left of a definition cannot rescue a calculation that went wrong on the right:

```cpp title="literal-type.cpp"
{{#include ../../examples/ch05/02-literal-type.cpp}}
```

```text title="Output"
{{#include ../../examples/ch05/02-literal-type.out}}
```

Both variables are `double`, but `1 / 2` divides two `int` literals. The division gives the integer 0, and only then is the 0 stored as a `double`. The second line has the literal `1.0`, so the division is a floating point division and gives 0.5. The rule from [lesson 4.8](../ch04-fundamental-data-types/08-floating-point-numbers.md) applies to literals just as it does to variables.

A suffix matters in the same way for large values. The product of 100000 and 100000 is 10 billion, which does not fit in an `int`, so the calculation overflows as [lesson 4.4](../ch04-fundamental-data-types/04-signed-integers.md) described. Writing `100000LL * 100000` makes one operand a `long long`, and the other is converted to match, so the calculation has room for the result.

## Literals and named constants

A literal is the right tool for a value that is obvious, such as 0, 1 or the 2 in "twice". It is the wrong tool for a value with a meaning, such as a fee or a limit. [Lesson 5.1](01-constant-variables-named-constants.md) showed how a named constant tells the reader what a number is for. The type of the constant then comes from its definition, as `const double pitchFee{25.0};` shows, and not from where the number is used.

<details>
<summary>Check your understanding</summary>

**Question 1.** What are the types of `7.5f`, `'7'` and `"7"`?

<details>
<summary>Answer</summary>

`7.5f` is a `float`, `'7'` is a `char`, and `"7"` is a string literal of the type `const char[2]`, which holds the character 7 and the null terminator.

</details>

**Question 2.** What does `double share{7 / 2};` store, and how do you get 3.5?

<details>
<summary>Answer</summary>

It stores 3, because both operands are `int` literals, so the division drops the fraction before the result is converted to `double`. Write `7.0 / 2` to make the division a floating point division.

</details>

**Question 3.** Why does `sizeof("hello")` give 6?

<details>
<summary>Answer</summary>

The string literal has five characters, and the compiler adds a null terminator after them, which makes six `char` values of one byte each.

</details>

</details>

## Summary

- Every literal has a type that the compiler chooses from how it is spelled, not from the variable that receives it.
- A suffix changes the type: `u` for unsigned, `L` and `LL` for the long types, and `f` for `float`.
- A string literal is a C-style string: an array of `char` that ends in a null terminator, which is why `"hello"` has a size of 6.
- The type of the literals decides the arithmetic, so `1 / 2` is 0 and `1.0 / 2` is 0.5.
- A literal is the right choice for an obvious value, and a named constant is the right choice for a value with a meaning.

## Further reading

- [Integer literals (cppreference)](https://en.cppreference.com/w/cpp/language/integer_literal)
- [Floating-point literals (cppreference)](https://en.cppreference.com/w/cpp/language/floating_literal)
- [String literals (cppreference)](https://en.cppreference.com/w/cpp/language/string_literal)
