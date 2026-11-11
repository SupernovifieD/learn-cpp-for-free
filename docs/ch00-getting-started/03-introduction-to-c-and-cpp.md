---
description: A short history of C and C++, the language standards from C++98 to C++26, the ideas behind C++ and the trade-offs that come with its power.
---

# 0.3 Introduction to C/C++

C++ did not appear from nowhere. It grew out of an earlier language called C, and it has been revised many times since. This lesson tells that story briefly, explains the ideas that shape the language, and sets honest expectations about what C++ is good at and where it can hurt you.

## The C language

C was created in the early 1970s at Bell Labs. It grew out of an earlier language called B, which had been designed to replace assembly language as the way to write system software for the Unix operating system, and in 1972 the language was renamed C. In 1973 Unix itself was rewritten in C, which showed that an operating system could be written in a higher-level language.

C spread widely, and different versions began to appear. A committee of the American National Standards Institute (ANSI) worked on a standard, and the ANSI C standard was published in 1989. The International Organization for Standardization (ISO) accepted it in 1990.

## The birth of C++

In 1979, Bjarne Stroustrup began the work that became C++, and the first version of the language was called "C with Classes." He was working at Bell Labs at the time, and he wanted to write efficient systems programs in the styles that an older language called Simula encouraged.

The first version of C++ was used inside AT&T in August 1983, and the name C++ followed late that year. The name signals that the language is an evolution of C: `++` is the C operator that increases a value by one.

## The C++ standards

Like C, C++ is defined by an international standard, and each new version of the standard is a new edition of the language. Editions are usually named after a year, so you will see names such as C++11 and C++20.

| Standard | Known for |
| --- | --- |
| C++98 (1998) | The first ISO standard for C++ |
| C++03 (2003) | A revision of C++98 that fixed defects |
| C++11 (2011) | A major update: `auto`, lambda expressions, rvalue references and `std::unique_ptr` |
| C++14 (2014) | A minor update with small improvements and defect fixes |
| C++17 (2017) | `std::optional`, structured bindings and the filesystem library |
| C++20 (2020) | Concepts, ranges, coroutines and modules |
| C++23 (2023) | `std::expected` and explicit object parameters |
| C++26 (in progress) | Still being finalized when this lesson was written |

The phrase **modern C++** usually means C++11 and the editions after it. This book teaches modern C++, using the C++20 edition.

!!! note
    The 2023 in the name C++23 is the year the committee finished its technical work. The ISO publication carries the year 2024, as ISO/IEC 14882:2024, because of administrative delay between final approval and publication.

You do not need to know what any of the features in the table mean yet. They are there so that you can see how the language has grown, and so that the names are familiar when you meet them later. The status of the newest edition changes, so check the [ISO C++ website](https://isocpp.org/std/the-standard) for the current state.

## What shapes the design of C++

A few ideas explain much of how C++ looks and behaves.

The first is the **zero-overhead principle**. It says that what you do not use, you do not pay for, and that what you do use could not be written any better by hand. In practice, C++ lets you build abstractions, such as reusable pieces of code with clear names, and aims for the result to run as fast as the hand-written version would.

The second is that C++ tends to assume you know what you are doing. It lets you work close to the hardware, and it does not add checks that you did not ask for, because every check would cost something.

The third is that C++ supports several styles of programming. You can write in a procedural style, organize data with classes, write reusable generic code or borrow ideas from functional programming. You will meet each of these styles in later chapters.

Finally, C++ stays compatible with C where it can. Stroustrup wanted C++ to be compatible with C, a complete language with enough performance and flexibility for even the most demanding systems programming. The standard C++ FAQ puts it as "as close as possible to compatible with C, but no closer."

## What C++ is used for

C++ shows up wherever speed and control over the hardware matter. Typical areas include:

- operating systems and their components,
- web browsers,
- video games and game engines,
- embedded systems, which are computers built into machines and devices,
- financial analysis and trading software,
- scientific computing and data analysis, and
- database systems.

You do not need to commit to any of these now. The skills you build in this book carry over to all of them.

## C and C++ are different languages

C++ is not a strict superset of C. There are valid C programs that are not valid C++, and a few pieces of code mean something different in the two languages. For example, C converts the `void*` pointer returned by `malloc` to any other pointer type without being asked, while C++ rejects that conversion unless you write it out explicitly.

For that reason, this book does not teach "C with classes." It teaches modern C++ as its own language, with its own recommended habits, and it will point out the places where C habits are best left behind.

## Power, performance and the price

The same features that make C++ fast and flexible make it demanding. The language has many features, and learning to use them well takes time.

The biggest hazard for beginners is **undefined behavior**. When a program breaks certain rules of the language, the standard places no requirements on what happens next. The program might crash, print nonsense, or appear to work until the day it does not, and the compiler is not required to warn you.

This book puts safe, modern practice first. You will turn on strict compiler warnings in lesson 0.11, prefer the standard library's tools over hand-made ones, and learn what causes undefined behavior so you can avoid it.

??? question "Check your understanding"
    What does the zero-overhead principle say?

    ??? success "Answer"
        What you do not use, you do not pay for, and what you do use could not be written any better by hand.

## Summary

- C was created in the early 1970s at Bell Labs and was used to rewrite the Unix operating system.
- Bjarne Stroustrup began work on "C with Classes" in 1979, and the language was named C++ in 1983.
- C++ has been standardized by ISO since 1998, and each new edition is named after a year, such as C++11 or C++20.
- C++ aims for zero overhead, trusts the programmer, supports several programming styles and stays close to C.
- C++ is not a strict superset of C, and this book teaches modern C++ rather than "C with classes."
- C++ gives you power and speed, along with hazards such as undefined behavior, so this book emphasizes safe, modern practice.

## Further reading

- [The Standard (isocpp.org)](https://isocpp.org/std/the-standard)
- [The standard C++ FAQ: big picture](https://isocpp.org/wiki/faq/big-picture)
- [Bjarne Stroustrup's C++ FAQ](https://www.stroustrup.com/bs_faq.html)
- [Applications written in C++ (Stroustrup)](https://www.stroustrup.com/applications.html)
- [C++ history (cppreference)](https://en.cppreference.com/w/cpp/language/history)
- [C history (cppreference)](https://en.cppreference.com/w/c/language/history)
