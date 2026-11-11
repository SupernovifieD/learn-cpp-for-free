---
description: What compiler extensions are, why to turn them off while you learn, and how to do it with GCC, Clang, Visual Studio and Visual Studio Code.
---

# 0.10 Configuring your compiler: Compiler extensions

Compilers do not only implement C++. Many of them also add features of their own, and by default they let you use those features without any complaint. This lesson explains why that can cause trouble while you are learning, and how to switch the extra features off.

## What compiler extensions are

A **compiler extension** is a feature that a compiler adds on top of the language standard. Extensions can be useful, but they are not part of standard C++, so another compiler may reject code that uses them, or may give it a different meaning.

Extensions matter to you for two reasons. The first is **portability**: code that relies on an extension works only with the compilers that support it. The second is that extensions blur what the language really is. If your compiler quietly accepts something that standard C++ does not allow, you can learn a habit that fails the first time you use another compiler.

For these reasons, this book asks you to turn extensions off, so that your compiler accepts standard C++ and tells you when you step outside it.

## An example: variable-length arrays

GCC and Clang accept a feature called a variable-length array. An **array** is a row of values stored one after another, and you will meet arrays in a later chapter. A variable-length array is one whose size is only known while the program runs.

Standard C++ does not allow this, because the size of an array has to be known when the program is compiled. Here is a program that uses it:

```cpp title="vla.cpp"
--8<-- "examples/ch00/10-vla.fail.cpp"
```

The first two lines are comments that the book's automated checks read. The first line says that the program must fail to build with the book's strict options. The second line lists the options that the checks remove to prove that the failure comes from them, so the same program has to build once `-pedantic-errors` and `-Werror` are gone.

When the strict options are on, the compiler reports the array as a problem. Clang, for example, says that variable-length arrays in C++ are an extension. Without them, the same compilers accept the line, because they treat it as a feature they offer.

## Turning extensions off

=== "Visual Studio"

    **Switch:** Open the project's property pages, choose **Configuration Properties**, then **C/C++**, then **Language**. Set **Conformance mode** to **Yes (/permissive-)**.

    **Note:** In recent versions of Visual Studio, choosing the C++20 standard turns this option on for you, but it does no harm to set it yourself. Apply the setting to all configurations, as lesson 0.9 advised.

=== "VS Code"

    **Switch:** Open the build task that your setup uses, which is stored in a file called `tasks.json`, and add the options from the **Command line** tab to the compiler's list of arguments.

    **Note:** Visual Studio Code only runs the compiler that you configured, so the options you pass are the options that apply.

=== "Command line"

    **Switch:** With GCC or Clang, add `-pedantic-errors`, which makes the compiler report code that does not follow the standard as an error. Run on the program above, this command fails.

    ```bash
    g++ -std=c++20 -pedantic-errors -o vla vla.cpp
    ```

    With Microsoft's compiler, add `/permissive-`, which asks it to follow the standard strictly.

    ```powershell
    cl /std:c++20 /EHsc /permissive- /Fe:vla.exe vla.cpp
    ```

    **Note:** The book's own flags in lesson 0.11 include `-pedantic-errors`, so you will not need to remember it separately.

## Standard modes and GNU modes

GCC and Clang choose the language standard with the `-std` option, and each standard comes in two spellings. A spelling such as `-std=c++20` selects the standard without extensions. A spelling such as `-std=gnu++20` selects the same standard with the GNU extensions switched on.

The default is not a standard-only mode. At the time of writing, GCC's documentation describes `gnu++20` as its default C++ dialect, and Clang's documentation lists `gnu++17`. Defaults differ between compilers and between versions of the same compiler, which is another reason to name the standard yourself. Lesson 0.12 explains how.

!!! best-practice "Best practice"
    Turn compiler extensions off and name the language standard explicitly, so that your compiler checks that your code is standard C++.

## Summary

- A compiler extension is a feature added to the standard language, and code that uses one may not work with another compiler.
- Turning extensions off makes your compiler accept standard C++ and report anything else.
- Variable-length arrays are a good example: GCC and Clang accept them as an extension, but standard C++ does not.
- Use `-pedantic-errors` with GCC and Clang, and `/permissive-` with Microsoft's compiler.
- `-std=c++20` selects the standard without extensions, while `-std=gnu++20` turns extensions on, and lesson 0.12 returns to this point.

## Further reading

- [GCC documentation: variable-length arrays](https://gcc.gnu.org/onlinedocs/gcc/Variable-Length.html)
- [GCC documentation: warning options, including -Wpedantic and -pedantic-errors](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html)
- [GCC documentation: C dialect options and the -std option](https://gcc.gnu.org/onlinedocs/gcc/C-Dialect-Options.html)
- [Microsoft documentation: /permissive- (standards conformance)](https://learn.microsoft.com/en-us/cpp/build/reference/permissive-standards-conformance)
