# 1.2 Comments

A **comment** is text in a program that the compiler ignores. It is written for the next person who reads the code, and that person is often you, a few weeks later, with no memory of why you wrote it that way. In this lesson you learn how to write comments, what they should say, and how to use them to switch code off while you experiment.

## Two kinds of comments

C++ has two ways to write a comment. A **line comment** starts with `//` and runs to the end of the line. A **block comment** starts with `/*`, ends with `*/`, and can span as many lines as you like.

This program uses both, and it uses a line comment in two different ways:

```cpp title="comments.cpp"
{{#include ../../examples/ch01/02-comments.cpp}}
```

The first two lines say what the file is and what it does, a habit that helps when you browse a folder full of programs. The block comment before `main` shows the second form. The comment at the end of the first output statement shares its line with code, which is fine as long as the line stays short. The program prints:

```text title="Output"
{{#include ../../examples/ch01/02-comments.out}}
```

Look at the second line inside `main`. It is an output statement with `//` in front of it, so the compiler never sees it, and the text it would have printed is missing from the output. That is called **commenting out** a statement.

## Block comments do not nest

A block comment ends at the first `*/` that the compiler finds. It does not count how many `/*` it has seen on the way, so you cannot put one block comment inside another. The standard says this plainly: these comments do not nest.

This surprises people when they switch off code that already contains a block comment. In the next program, the outer comment is meant to switch off two statements, and the second statement ends with a comment of its own:

```cpp title="nested-comment.cpp"
{{#include ../../examples/ch01/02-nested-comment.fail.cpp}}
```

The `*/` after "the second one" ends the outer comment as well. That makes `return 0;` real code again, and the last `*/` is stray text that the compiler cannot make sense of, so it reports errors. It also warns about the `/*` that it found inside a comment, because that is almost always a mistake.

> [!TIP]
> To switch off a stretch of code that already contains block comments, put `//` in front of each of its lines instead of wrapping the stretch in `/* ... */`. Most editors can add and remove `//` on all the selected lines at once.

## What good comments say

The most useful comment explains **why** the code is the way it is, not **what** it does. A reader can see what a statement does by reading it. What the reader cannot see is the reason behind it: a rule from somewhere else, a choice between two options, a trap that you found the hard way.

A comment that repeats the code is clutter:

```cpp
// Print the late fee.
std::cout << "Late fee: 25 cents per day\n";
```

A comment that gives the reason is worth keeping:

```cpp
// The library board fixes this fee; change the text when the board does.
std::cout << "Late fee: 25 cents per day\n";
```

Two other kinds of comments are worth writing. At the top of a file, a line or two can say what the program does. Once you write your own functions in Chapter 2, a short comment above each one can say what it does, what it needs and what it gives back, so that a reader can use the function without reading its body.

> [!BEST-PRACTICE]
> Write comments that explain why, and write code that is clear enough to show what. When you change code, change the comments next to it, because a comment that no longer matches the code is worse than no comment at all.

## Switching code off while you experiment

Comments are also a quick way to try something out. If you are not sure whether a statement is the cause of a problem, comment it out, build the program and run it again. If the problem is gone, you know where to look, and you can remove the `//` to bring the statement back.

This is fine for a short experiment. Do not leave stretches of commented-out code in a finished program, because readers cannot tell whether the old code matters. Chapter 3 shows better ways to find the cause of a problem, and it replaces most of this kind of guessing.

<details>
<summary>Check your understanding</summary>

**Question 1.** What does this fragment print?

```cpp
std::cout << "A\n"; // std::cout << "B\n";
// std::cout << "C\n";
std::cout << "D\n";
```

<details>
<summary>Answer</summary>

It prints `A` and `D`, each on its own line. The text after `//` on the first line is a comment, and so is the whole second line.

</details>

**Question 2.** Which of these two comments is better, and why?

```cpp
// Add one to the page count.
// The index page is not numbered, so the count starts one page late.
```

<details>
<summary>Answer</summary>

The second one. The first only repeats what a statement would already say, while the second gives a reason that the code alone cannot show.

</details>

</details>

## Summary

- The compiler ignores comments, so they are for human readers.
- A line comment starts with `//` and ends with the line, and a block comment sits between `/*` and `*/`.
- Block comments do not nest: the first `*/` ends the comment, and whatever follows is code.
- Good comments explain why, describe the purpose of a file or function in a line or two, and stay true when the code changes.
- Commenting out a statement is a quick way to experiment, but finished programs should not keep dead code.

## Further reading

- [Comments (cppreference)](https://en.cppreference.com/w/cpp/comment)
