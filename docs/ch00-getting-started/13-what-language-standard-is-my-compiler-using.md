---
description: How to find out which C++ standard your compiler is using, with the __cplusplus macro, Microsoft's _MSVC_LANG and a short program that prints the result.
---

# 0.13 What language standard is my compiler using?

You have chosen a standard, but did your compiler really apply it? This lesson shows how to ask the compiler which standard it is using, and it ends with a small program that prints the answer. You will not need to understand every line of that program yet.

## Why you might need to know

There are three common reasons to check. The first is to confirm that your settings took effect, because a setting in the wrong place is a common slip. The second is to find out why a feature from a newer standard does not compile. The third is to learn what a compiler does when you do not name a standard at all, as lesson 0.12 described.

## The `__cplusplus` macro

A **macro** is a name that the compiler replaces with some other text before it translates your code. You will learn how to write macros much later. For now, it is enough to know that compilers define some of them for you.

Every C++ compiler defines a macro named `__cplusplus`. Its value is a number that depends on the standard in use:

| Value | Standard |
| --- | --- |
| `199711L` | C++98 and C++03 |
| `201103L` | C++11 |
| `201402L` | C++14 |
| `201703L` | C++17 |
| `202002L` | C++20 |
| `202302L` | C++23 |

The `L` at the end of each value marks it as a number of a type called `long`. It is part of how the value is written in code, and you will not see it when the number is printed.

The value for C++26 is not final. The documentation of GCC and cppreference gives `202603L`, but C++26 was not yet published when this lesson was written, and compilers have printed other values for it, so check your compiler's documentation. A value that falls between two rows of the table usually means that the compiler implements only part of the newer standard. GCC 13, for example, prints `202100L` when you ask for C++23, because its support for C++23 was still partial.

## Microsoft's compiler

Microsoft's compiler is a special case. To avoid breaking old code that depends on the macro, it keeps `__cplusplus` at `199711L` unless you opt in with the `/Zc:__cplusplus` option.

It also defines a second macro, `_MSVC_LANG`, which always reports the standard in use. Its value is `201402L` by default or with `/std:c++14`, `201703L` with `/std:c++17` and `202002L` with `/std:c++20`. With `/std:c++latest` it is set to a higher value that Microsoft does not specify.

## A program that prints the standard

This program prints the value of the macro and the name of the matching standard. It uses `_MSVC_LANG` when it exists, and `__cplusplus` otherwise.

```cpp title="print-standard.cpp"
--8<-- "examples/ch00/13-print-standard.cpp"
```

Lines that begin with `#`, such as `#if` and `#else`, are instructions for the compiler about which code to keep. The program keeps one of the two definitions of `standard`, depending on the compiler. The chain of `if` and `else if` statements then picks the first name that fits, starting from the newest. You will learn how they work in later chapters.

Build the program with the options from lesson 0.11. If you build it as C++20, it prints this:

```text title="Output (example)"
Language standard value: 202002
C++20
```

This output is only an example, because it depends on your compiler and the options you pass. Build with `-std=c++17`, and the program prints `201703` and `C++17`. If you build without naming a standard, you see the default of your compiler, which is a good way to find out what that default is.

!!! tip
    Run the program once for every standard your compiler supports, and compare the numbers with the table above.

## You are ready for Chapter 1

You now have a compiler, an editor and a build that you understand, and you know how to set up your tools for learning. Take a moment to look back at the [overview of this chapter](index.md), where you can revisit any lesson. Then you are ready for the next step: writing programs of your own.

## Summary

- Compilers define the macro `__cplusplus`, and its value tells you which standard is in use.
- The values are `199711L` for C++98 and C++03, then `201103L`, `201402L`, `201703L`, `202002L` and `202302L` for C++11 through C++23.
- The value for C++26 is not final, and a value between two standards means partial support for the newer one.
- Microsoft's compiler keeps `__cplusplus` at `199711L` unless you use `/Zc:__cplusplus`, but `_MSVC_LANG` always reports the standard.
- The example program prints the value and the matching name, and its output depends on your compiler and options.

## Further reading

- [cppreference: predefined macros, including __cplusplus](https://en.cppreference.com/w/cpp/preprocessor/replace)
- [GCC documentation: standard predefined macros](https://gcc.gnu.org/onlinedocs/cpp/Standard-Predefined-Macros.html)
- [Microsoft documentation: /Zc:__cplusplus](https://learn.microsoft.com/en-us/cpp/build/reference/zc-cplusplus)
- [Microsoft documentation: predefined macros, including _MSVC_LANG](https://learn.microsoft.com/en-us/cpp/preprocessor/predefined-macros)
