# 2.9 Naming collisions and an introduction to namespaces

Names are a limited resource. Every function, variable and type in a program needs one, and a large program, with the Standard Library and perhaps other libraries behind it, contains thousands of them. Sooner or later two things end up with the same name. This lesson shows what happens then, and it introduces the feature that C++ provides to keep names apart: the namespace.

## Naming collisions

A **naming collision** happens when two different things in a program are given the same name, in a place where the name has to mean one thing. You have already seen one kind in lesson 2.7. A file that defines the same function twice is rejected by the compiler, which reports a redefinition.

The other kind is harder to notice. Each source file is compiled on its own, so the compiler cannot see that two files both define a function with the same name. Every file compiles without a complaint, and the problem shows up in the last step. These three files form one program, in which the files `first.cpp` and `second.cpp` both define a function called `pick`:

```cpp title="first.cpp"
{{#include ../../examples/ch02/09-collision.fail/first.cpp}}
```

```cpp title="second.cpp"
{{#include ../../examples/ch02/09-collision.fail/second.cpp}}
```

```cpp title="main.cpp"
{{#include ../../examples/ch02/09-collision.fail/main.cpp}}
```

Compiling each file alone works, but building the whole program fails. The linker finds two definitions of `pick`, and it cannot tell which one the call in `main` is meant to reach, so it stops with an error that says the function is defined twice. The wording differs between linkers, and some of them name the two files that clash.

In a program that you write alone, you can fix this by renaming one of the functions. In a program that combines your code with code from other people, a collision is a real danger, because you cannot see every name that the others use.

## Namespaces

C++ solves the problem with **namespaces**. A namespace is a named region that holds names. Two things with the same name can live in two different namespaces without clashing, in the same way that two people with the same first name are told apart by their family names.

You have been using a namespace since your first program: `std`. The Standard Library puts all of its names, such as `cout` and `cin`, into the namespace `std`, so that they cannot clash with the names that you choose.

Names that you define yourself, outside of any namespace, belong to the **global namespace**. When you write the function `printGreeting` at the top level of a file, as in lesson 2.1, it goes into the global namespace, together with `main` and every other function in your examples.

## The scope resolution operator

To use a name from a namespace, you write the name of the namespace, two colons and the name. The two colons are the **scope resolution operator**, written `::`:

```cpp
std::cout << "Hello\n";
```

The name `std::cout` says "the `cout` that lives in `std`". If you define a function or a variable of your own with the name `cout`, it is a different thing, and the two do not clash, because the one in the library is always written with its namespace. This is why every example in this book has `std::` in front of the library's names.

A name with `::` and nothing in front of it, as in `::pick`, refers to the global namespace explicitly. You will rarely need that form, but it shows that the global namespace is a namespace like any other.

## Why the book avoids using namespace std

Typing `std::` many times can feel tiresome, and C++ offers a shortcut. A **using directive** makes all the names of a namespace available without the prefix:

```cpp
using namespace std;
```

After this line, you can write `cout` instead of `std::cout`. Many tutorials and programs do this, and you will see it in other people's code. This book does not, for a good reason, which the next program shows. It defines a variable called `cout` of its own, and the using directive brings the library's `cout` into the same place:

```cpp title="using-directive.cpp"
{{#include ../../examples/ch02/09-using-directive.fail.cpp}}
```

The compiler refuses to build it. In `main`, the name `cout` now means two different things, the variable and the library's stream, and the compiler reports that the reference is ambiguous. The program would have worked without the using directive, because `std::cout` would not have clashed with the variable.

The Standard Library has thousands of names, and new versions of the language add more. A program that compiles today with a using directive can fail tomorrow, when a new name in `std` happens to match one of yours. The collision appears in a program that you have not changed, and that makes it hard to explain.

> [!BEST-PRACTICE]
> Write `std::` in front of the names of the Standard Library, and do not use `using namespace std;`. The extra typing is small, and it keeps your names and the library's names apart.

## Your own namespaces

You can also define namespaces of your own, so that the functions of one part of a program do not clash with those of another. That is how libraries protect their names. Defining your own namespaces is a topic for Chapter 7. For now, the important points are that the Standard Library lives in `std`, that `::` selects a name from a namespace, and that a using directive is better left out.

<details>
<summary>Check your understanding</summary>

**Question 1.** Two source files each define a function named `pick`. Each file compiles on its own. When is the problem found, and by which tool?

<details>
<summary>Answer</summary>

It is found when the program is linked, by the linker. The compiler only sees one file at a time, so it cannot know that the other file has a function with the same name. The linker then finds two definitions of `pick`.

</details>

**Question 2.** What does the name `std::cout` mean, and what is the `::` called?

<details>
<summary>Answer</summary>

It means the name `cout` in the namespace `std`, which is the output stream of the Standard Library. The `::` is called the scope resolution operator.

</details>

**Question 3.** Why does this book write `std::cout` and avoid `using namespace std;`?

<details>
<summary>Answer</summary>

A using directive makes every name of the Standard Library available without a prefix, so one of them can clash with a name that you define, and a later version of the library can add a name that clashes. Writing the prefix keeps the two sets of names apart.

</details>

</details>

## Summary

- A naming collision is two things with the same name where the name must mean one thing, and a collision between two files is found by the linker.
- A namespace is a named region that holds names, so that equal names in different namespaces do not clash.
- The Standard Library puts its names in `std`, and your own top-level names are in the global namespace.
- The scope resolution operator `::` selects a name from a namespace, as in `std::cout`.
- A using directive makes all the names of a namespace visible without the prefix, which invites collisions, so the book writes `std::` instead.
- Your own namespaces are introduced in Chapter 7.

## Further reading

- [Namespaces (cppreference)](https://en.cppreference.com/w/cpp/language/namespace)
- [Qualified name lookup (cppreference)](https://en.cppreference.com/w/cpp/language/qualified_lookup)
