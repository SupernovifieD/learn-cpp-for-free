# 2.6 Why functions are useful, and how to use them effectively

You now know how to write a function, how to pass values into it and how to get a value out. This lesson steps back from the mechanics and asks a different question: when should you write a function at all? It gives you the reasons that make functions worth the effort, and a few guidelines that keep them useful as your programs grow.

## What functions give you

Functions are not only a way to save typing. They change the way that a program can be built and maintained.

**Organization.** A program that is split into functions reads like an outline. The statements of `main` tell the story at a high level, and each function holds the details of one step. A reader can understand what the program does without reading every line of how it does it.

**Reuse.** A function that is written once can be called from many places, and from many programs. You do not repeat the work, and you do not repeat the mistakes either.

**Testing.** A small function with clear inputs and an output can be tried on its own. You call it with values for which you know the answer and compare the result, long before the rest of the program exists.

**Simpler changes.** When a rule changes, such as how a total is calculated, a function that holds that rule is the only place that needs to be edited. Without it, you have to find every copy of the rule, and you will miss one.

**Abstraction.** A caller needs to know what a function does, and not how it does it. That lets you use a function whose inside you have forgotten, or have never read, and it lets the author replace the inside later without breaking anything.

## Before and after

The best way to see the difference is to compare two versions of a program that do the same work. The first one repeats the same two output statements for each of three items:

```cpp title="before.cpp"
{{#include ../../examples/ch02/06-before.cpp}}
```

```text title="Output"
{{#include ../../examples/ch02/06-before.out}}
```

The second version moves the repeated statements into a function, `printCost`, and calls it with the amount and the price of each item:

```cpp title="after.cpp"
{{#include ../../examples/ch02/06-after.cpp}}
```

```text title="Output"
{{#include ../../examples/ch02/06-after.out}}
```

The two programs print exactly the same output. What changed is the program.

The second version is shorter, and `main` reads like a list of items. The calculation of the cost is written once, so if the rule changes, for example because the prices include a fee, there is a single line to edit. The first version has three copies of the rule, and a change to one of them can be forgotten in the others.

> [!KEY-INSIGHT]
> When you copy a group of statements and change a few values, you are looking at a function whose parameters are the values that you changed.

## Guidelines for good functions

**Give a function one job.** A function that does one thing is simple to name, to test and to reuse. If you describe a function and the description has an "and" in it, such as "reads the numbers and prints the average", consider two functions.

**Name a function with a verb.** A function does something, so its name should say what: `printCost`, `readNumber`, `totalPrice`. A reader who sees `totalPrice(tickets, price)` knows what the line does without looking at the function.

**Turn repeated code into a function.** The moment you write the same statements a second time, you have a candidate. Doing it for the third time is a sign that you should already have done it.

**Split a function that grows too long.** There is no exact number of lines that is too many, but a function that you cannot read in one screen probably does several jobs. Look for the steps inside it and give each step a name.

**Keep a function self-contained.** A function should get what it needs through its parameters and give its result through its return value, as lesson 2.5 explained. Then it can be understood, tested and moved without looking at the code around it.

> [!BEST-PRACTICE]
> Name a function with a verb that says what it does, and give it one job. If you cannot name it clearly, it is probably doing too much.

<details>
<summary>Check your understanding</summary>

**Question 1.** Give two reasons why the second version of the program is better than the first.

<details>
<summary>Answer</summary>

The calculation of the cost is written once, so a change to the rule needs a single edit instead of three. The `main` function is also shorter and reads like a list of items, because the details are in `printCost`.

</details>

**Question 2.** A function is described as "reads two numbers and prints their sum". What guideline does this description break, and what could you do?

<details>
<summary>Answer</summary>

It has two jobs, which the "and" shows. You could write one function that reads a number and returns it, one that adds two numbers and returns the sum, and let `main` print the result.

</details>

**Question 3.** What does this call print, when `printCost` is the function of the second program above?

```cpp
printCost(4, 5);
```

<details>
<summary>Answer</summary>

It prints `  amount: 4` on one line and `  cost: 20 euros` on the next, because 4 times 5 is 20.

</details>

</details>

## Summary

- Functions give a program structure, let you reuse work, make small pieces testable and simplify changes.
- A caller needs to know what a function does, not how it does it, and that is called abstraction.
- Repeated statements that differ only in a few values are a function with those values as parameters.
- A function should have one job, a name that starts with a verb, and a reasonable length.
- A function that gets its input through parameters and gives its output through a return value is the simplest kind to use and to test.
