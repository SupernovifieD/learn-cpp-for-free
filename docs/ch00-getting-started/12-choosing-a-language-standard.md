# 0.12 Configuring your compiler: Choosing a language standard

Lesson 0.3 explained that C++ comes in editions, and that each edition is named after a year. Your compiler can build code for several of them, so you have to tell it which one to use. This lesson shows how to choose, and it explains the choice that this book makes.

## What a language standard is

A **language standard** is the official definition of one edition of C++. It describes what the language and its Standard Library must do, and compiler makers implement it. When you select a standard, you ask the compiler to accept the features of that edition and to apply its rules.

You might wonder why you cannot always use the newest edition. The answer is that a newer edition can add features that your compiler does not support yet. A program written for the newest edition may also fail to build on a computer with an older compiler.

## Naming the standards

Each toolchain has its own spelling for choosing a standard. GCC and Clang use the `-std` option, and Microsoft's compiler uses `/std`.

### GCC and Clang

| Standard | Option |
| --- | --- |
| C++11 (2011) | `-std=c++11` |
| C++14 (2014) | `-std=c++14` |
| C++17 (2017) | `-std=c++17` |
| C++20 (2020) | `-std=c++20` |
| C++23 (2023) | `-std=c++23` |
| C++26 (in progress) | `-std=c++2c` |

### Microsoft's compiler

| Standard | Option |
| --- | --- |
| C++14 (2014) | `/std:c++14` (default) |
| C++17 (2017) | `/std:c++17` |
| C++20 (2020) | `/std:c++20` |
| C++23 (2023) | `/std:c++23preview` |
| C++26 (in progress) | `/std:c++latest` |

Microsoft's compiler has no option for C++11, and `/std:c++14` is the oldest one that it offers.

Standards that are still being finished have working names. The letter in a working name counts the editions of the 2020s, so `c++2a` is the first of them, C++20, `c++2b` is C++23 and `c++2c` is C++26. Older compilers only understand these working names, and newer ones keep them as deprecated aliases. Recent versions of GCC also accept `-std=c++26`.

Microsoft's `/std:c++latest` turns on all the features of the next standard that the compiler implements so far. Its `/std:c++23preview` option enables the C++23 features that are implemented, and Microsoft's documentation says it will become `/std:c++23` later.

## Why compilers lag behind

A standard becomes official on a particular day, but compiler makers need time to implement it. Each feature arrives in a particular compiler version, so the same standard can be fully supported by one compiler and only partly supported by another. For this reason, the C++23 and C++26 rows of the table are the ones most likely to give you trouble.

The [C++ compiler support tables on cppreference](https://en.cppreference.com/w/cpp/compiler_support) list, for each feature, the first version of every major compiler that supports it.

## This book's choice

This book uses **C++20**. It is a major edition with many modern features, and compilers have supported most of its features for several years, so it works on nearly every current setup. You are welcome to use a newer standard if your compiler supports it, and you will not lose anything by doing so.

## Standard modes and GNU modes

Lesson 0.10 introduced the two spellings that GCC and Clang accept for each standard. `-std=c++20` selects the standard on its own, while `-std=gnu++20` selects it together with the compiler's own extensions.

The default is usually a GNU mode, and it changes between versions. Clang's documentation lists `gnu++17` as its default, GCC's documentation says `gnu++20` for its newest releases, and Microsoft's compiler defaults to C++14. Because the defaults differ, always name the standard yourself, and use the `c++` spelling to keep extensions off.

> [!BEST-PRACTICE]
> Always set the language standard explicitly, and prefer `-std=c++20` over `-std=gnu++20` while you learn.

## Setting the standard

{{#tabs}}
{{#tab Visual Studio}}

**Switch:** Open the project's property pages, choose **Configuration Properties**, then **C/C++**, then **Language**. In **C++ Language Standard**, choose **ISO C++20 Standard** from the list.

**Note:** Choose **All Configurations** first, as lesson 0.9 explained, so that Debug and Release agree.

{{#endtab}}
{{#tab VS Code}}

**Switch:** Add the option from the **Command line** tab to the list of compiler arguments in your build task, for instance `-std=c++20`.

**Note:** The C/C++ extension also has a setting for the standard that it uses to analyze your code. Set it to the same value so that the editor and the compiler agree.

{{#endtab}}
{{#tab Command line}}

**Switch:** Put the option before the file name.

```bash
g++ -std=c++20 -o hello-world hello-world.cpp
clang++ -std=c++20 -o hello-world hello-world.cpp
```

```powershell
cl /std:c++20 /EHsc /Fe:hello-world.exe hello-world.cpp
```

**Note:** If your compiler rejects the option, it is probably too old to know C++20. Update it, as lesson 0.6 suggested.

{{#endtab}}
{{#endtabs}}

## Summary

- A language standard is the official definition of one edition of C++, and you choose which one your compiler follows.
- GCC and Clang use `-std=c++20` and Microsoft's compiler uses `/std:c++20`, with working names such as `c++2a` for editions that are still being finished.
- Compilers implement new editions gradually, so newer standards are less likely to work everywhere.
- This book uses C++20, and you may use a newer standard if your compiler supports it.
- Defaults differ between compilers, so always set the standard yourself, and prefer `c++20` to `gnu++20`.

## Further reading

- [GCC documentation: C dialect options and the -std option](https://gcc.gnu.org/onlinedocs/gcc/C-Dialect-Options.html)
- [GCC documentation: C++ language status](https://gcc.gnu.org/projects/cxx-status.html)
- [Clang documentation: C++ status](https://clang.llvm.org/cxx_status.html)
- [Microsoft documentation: /std (specify language standard version)](https://learn.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version)
- [C++ compiler support (cppreference)](https://en.cppreference.com/w/cpp/compiler_support)
