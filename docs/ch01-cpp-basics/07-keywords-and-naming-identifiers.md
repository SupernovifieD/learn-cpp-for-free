# 1.7 Keywords and naming identifiers

Every variable needs a name, and later in this book so will every function. C++ lets you choose most of these names yourself, but it has rules about what a name may look like and a few words that you may not use at all. This lesson explains the rules, the names that you should avoid even though the compiler accepts them, and how to choose names that make a program readable.

## Identifiers and keywords

A name that you choose for a variable, a function or another thing in your program is called an **identifier**. In `int bookCount{42};`, the word `bookCount` is an identifier, and so is `main`.

Some words are not yours to choose. A **keyword** is a word that has a fixed meaning in the language, and you cannot use it as an identifier. You have already met two of them, `int` and `return`, and others such as `if` and `class` are coming in later chapters. C++ has a long list of keywords, and you do not need to learn it by heart. The compiler tells you when you use one by mistake, and cppreference keeps a [complete list of the keywords](https://en.cppreference.com/w/cpp/keyword).

A few words are only special in certain places. The words `override` and `final`, for example, have a meaning in the middle of a class definition, and anywhere else they are ordinary identifiers. These are called identifiers with special meaning, and you will meet them much later.

## Rules for identifiers

An identifier follows these rules:

- It may contain letters, digits and the underscore character `_`, and nothing else. In particular, it cannot contain spaces.
- It cannot start with a digit.
- It cannot be a keyword.
- It is case-sensitive, so `total`, `Total` and `TOTAL` are three different names.

The program below breaks the first rule: the name `first place` contains a space, so the compiler reads it as two separate words and cannot make sense of the definition.

```cpp title="bad-identifier.cpp"
{{#include ../../examples/ch01/07-bad-identifier.fail.cpp}}
```

The other rules are broken in the same way. Each of these lines is rejected by the compiler:

```cpp
int 2ndPlace{2};
int class{2};
int total-cost{2};
```

The first name starts with a digit, the second one is a keyword, and the third contains a hyphen, which C++ reads as the minus operator.

## Names that the compiler accepts but you should avoid

The standard reserves some names for the compiler and the Standard Library, so that they can use them without clashing with yours. A name is reserved when it:

- contains two underscores in a row, anywhere in the name, or
- starts with an underscore followed by an uppercase letter, or
- starts with an underscore at the top level of a program, outside of any function.

Your compiler may accept such a name today. But if you use it, your program can clash with a name that the compiler or the library uses, and the result is an error that is difficult to explain. The simplest rule is to avoid underscores at the beginning of a name, and to avoid double underscores altogether.

## Choosing good names

Two styles are common among C++ programmers. In **camelCase**, words are joined and each new word starts with a capital letter: `bookCount`. In **snake_case**, words are separated by underscores: `book_count`. Both are legal, and both are used in large projects. This book uses camelCase for variables and functions.

The important thing is to pick one style and stick with it, because a program in which `bookCount` and `seat_total` appear together is harder to read than one that uses a single style. When you work on someone else's code, follow the style that is already there.

Beyond the style, a name should say what the variable holds. The table shows how small changes help:

| Poor name | Better name | Why |
| --- | --- | --- |
| `x` | `freeSeats` | A letter says nothing about the content |
| `n2` | `reservedSeats` | A number says how it was made, not what it is |
| `data` | `bookCount` | A vague word could mean anything |

A name should be as long as it needs to be, and no longer. A variable that lives for three lines can have a short name, while one that is used all over a long program deserves a name that tells the reader what it is without a search. Avoid abbreviations that only you understand, because the next reader, which may be you, will not remember them.

> [!BEST-PRACTICE]
> Choose a name that says what the variable holds, written in the style that your project uses. A good name saves a comment.

<details>
<summary>Check your understanding</summary>

**Question 1.** Which of these are valid identifiers: `price2`, `2price`, `total cost`, `class`, `Total`?

<details>
<summary>Answer</summary>

Only `price2` and `Total` are valid. `2price` starts with a digit, `total cost` contains a space, and `class` is a keyword.

</details>

**Question 2.** The compiler accepts the name `_Count` in a program. Should you use it?

<details>
<summary>Answer</summary>

No. A name that starts with an underscore followed by an uppercase letter is reserved for the compiler and the Standard Library, so it can clash with a name they use even though your compiler accepts it today.

</details>

**Question 3.** Are `seats` and `Seats` the same variable?

<details>
<summary>Answer</summary>

No. C++ is case-sensitive, so they are two different names.

</details>

</details>

## Summary

- An identifier is a name that you choose, and a keyword is a word with a fixed meaning that you cannot use as a name.
- An identifier contains letters, digits and underscores, does not start with a digit, is not a keyword, and is case-sensitive.
- Names with a double underscore, or with an underscore followed by an uppercase letter, are reserved, and so are names that start with an underscore at the top level.
- camelCase and snake_case are both common, and this book uses camelCase, because consistency matters more than the choice.
- A good name says what the variable holds, and its length should match how widely it is used.

## Further reading

- [Identifiers (cppreference)](https://en.cppreference.com/w/cpp/language/identifiers)
- [Keywords (cppreference)](https://en.cppreference.com/w/cpp/keyword)
