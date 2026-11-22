# 4.x Chapter 4 summary and quiz

This page recaps the lessons of Chapter 4 and then tests what you remember. The summary names the key terms of each lesson, so use it to find a lesson that you want to read again.

The quiz has eight questions in rising difficulty: the first three are about ideas, the next two are about reading and repairing programs, and the last three ask you to write a program. Try each question before you open its solution.

## Summary

- [4.1 Introduction to fundamental data types](01-introduction-to-fundamental-data-types.md): memory holds bits, and a type says how many bits an object uses and how to read them. The fundamental types are integer, floating point, boolean, character and `void`, and the integral types include `bool` and `char`.
- [4.2 Void](02-void.md): `void` stands for no value. A function can return it, and a variable cannot have it as its type.
- [4.3 Object sizes and the sizeof operator](03-object-sizes-and-the-sizeof-operator.md): n bits hold 2 multiplied by itself n times patterns, so size limits range. The standard sets only minimum sizes, and `sizeof` reports a size in bytes as a `std::size_t`.
- [4.4 Signed integers](04-signed-integers.md): `short`, `int`, `long` and `long long` hold negative numbers with two's complement. A signed overflow is undefined behavior.
- [4.5 Unsigned integers, and why to avoid them](05-unsigned-integers-and-why-to-avoid-them.md): unsigned arithmetic wraps around, and mixing it with signed values turns negative numbers into huge ones. Prefer signed types for quantities.
- [4.6 Fixed-width integers and size_t](06-fixed-width-integers-and-size-t.md): `<cstdint>` offers types such as `std::int32_t` with an exact size. `std::int8_t` prints as a character, and `std::size_t` is the type of sizes.
- [4.7 Introduction to scientific notation](07-introduction-to-scientific-notation.md): a significand and an exponent give a short form for large and small numbers. `1.2e3` is a `double` literal, and `std::cout` prints six significant digits.
- [4.8 Floating point numbers](08-floating-point-numbers.md): `float` and `double` store numbers with a fractional part, with rounding errors. `std::setprecision` changes the digits shown, and the book prefers `double`.
- [4.9 Boolean values](09-boolean-values.md): a `bool` is `true` or `false`, and a comparison produces one. `std::boolalpha` prints and reads the words, and `!` negates.
- [4.10 Introduction to if statements](10-introduction-to-if-statements.md): `if`, `else` and `else if` run a block only when a condition holds. The first true condition of a chain wins, and `=` is not `==`.
- [4.11 Chars](11-chars.md): a `char` holds the code of a character, and arithmetic on it gives an `int`. Escape sequences write characters such as a new line, and single quotes make a `char`.
- [4.12 Introduction to type conversion and static_cast](12-introduction-to-type-conversion-and-static-cast.md): the compiler converts values implicitly, and the book's options reject the risky conversions. `static_cast<type>(value)` converts on purpose.

## Quiz

### Question 1

Choose the best type for each quantity: `int`, `double`, `bool`, `char` or `std::int64_t`.

- (a) The number of seats in a theater.
- (b) The length of a table in meters, with a fraction.
- (c) Whether the door is open.
- (d) The letter that grades a test.
- (e) A counter of downloads that may pass 5 billion.

<details>
<summary>Solution</summary>

- (a) `int`: it is a whole number that stays far below the range of an `int`.
- (b) `double`, because the value has a fractional part.
- (c) `bool`, which has exactly the two values that the question needs.
- (d) `char`, which holds one character.
- (e) `std::int64_t`: the value does not fit in 32 bits, and a `long` has only 32 bits on 64-bit Windows, so the fixed-width type is the only choice that is the same on every platform.

</details>

### Question 2

A program defines `unsigned int stock{2};` and then runs `stock = stock - 3;`. What does `stock` hold afterwards if an `unsigned int` has 32 bits? What would an `int` hold in the same situation?

<details>
<summary>Solution</summary>

The `unsigned int` holds 4,294,967,295. Two minus three is -1, which is below the range, so the unsigned arithmetic wraps around to the largest value. An `int` would hold -1. The wraparound is defined behavior, so no tool reports it, and the shop that the number describes now seems to have four billion items.

</details>

### Question 3

What does this fragment print?

```cpp
std::cout << 9 / 4 << " " << 9 / 4.0 << " " << 2.5e2 << "\n";
```

<details>
<summary>Solution</summary>

It prints `2 2.25 250`. In `9 / 4` both operands are integers, so the fraction is dropped. In `9 / 4.0` one operand is a `double`, so the division keeps the fraction. The literal `2.5e2` is 2.5 times 10 to the power of 2, which is 250, and `std::cout` prints it in plain form because it has fewer than six digits.

</details>

### Question 4

Read the program, and say what it prints.

```cpp title="shipping.cpp"
{{#include ../../examples/ch04/x-q4-shipping.cpp}}
```

<details>
<summary>Solution</summary>

The program prints `Parcel`. The computer tests the conditions from the top and runs the block of the first one that is true. The test `weightKg > 20` is false, and the test `weightKg > 10` is true, so the chain stops there, even though 12 is also greater than 2. The conditions of a chain must be in the right order.

```text title="Output"
{{#include ../../examples/ch04/x-q4-shipping.out}}
```

</details>

### Question 5

The program below should print the average of 7 and 2, which is 3.5. The compiler refuses to build it. Find the problem and fix it.

```cpp title="average-bug.cpp"
{{#include ../../examples/ch04/x-q5-average.fail.cpp}}
```

<details>
<summary>Solution</summary>

There are two problems in the same line. The expression `total / count` divides two integers, so its value is the integer 3 and the fraction is already gone. And a brace initializer does not accept a calculated `int` for a `double`, which is why the compiler stops. Convert one operand to `double` before the division, so that the division is a floating point division:

```cpp title="average-fixed.cpp"
{{#include ../../examples/ch04/x-q5-average-fixed.cpp}}
```

```text title="Output"
{{#include ../../examples/ch04/x-q5-average-fixed.out}}
```

</details>

### Question 6

Write a program that asks for a temperature in whole degrees and prints `Freezing` below 0, `Cold` below 15, `Mild` below 25 and `Warm` otherwise. Type 18 and press Enter when you test it.

<details>
<summary>Solution</summary>

A chain of `if`, `else if` and `else` does the job. The conditions go from the lowest limit to the highest, so each one only needs to test its own upper limit: a temperature that reaches the third test is already known to be 0 or more.

```cpp title="temperature.cpp"
{{#include ../../examples/ch04/x-q6-temperature.cpp}}
```

```text title="Example session"
{{#include ../../examples/ch04/x-q6-temperature.session}}
```

</details>

### Question 7

Write a program that asks for the number of seats sold and the number of shows, and prints the average number of seats per show as a number with a fractional part. Type 7 and 2 when you test it. If the number of shows is not positive, print a message and end the program with the exit status 1.

<details>
<summary>Solution</summary>

The check comes first, because a division by zero must never happen, and an early `return` leaves the program. To keep the fraction, the program converts `seatsSold` to `double` with `static_cast`, so that the division is a floating point division.

```cpp title="seat-average.cpp"
{{#include ../../examples/ch04/x-q7-seat-average.cpp}}
```

```text title="Example session"
{{#include ../../examples/ch04/x-q7-seat-average.session}}
```

</details>

### Question 8

Write a program that reads one letter, prints its code, and prints the next letter of the alphabet. Type `m` and press Enter when you test it.

<details>
<summary>Solution</summary>

`std::cin >> letter` reads one character. The code is the letter converted to `int`, and the next letter is the sum `letter + 1`, which is an `int` and has to be converted back to `char` with `static_cast`, or the brace initializer would refuse it. The code of `m` is 109 in ASCII.

```cpp title="next-letter.cpp"
{{#include ../../examples/ch04/x-q8-next-letter.cpp}}
```

```text title="Example session"
{{#include ../../examples/ch04/x-q8-next-letter.session}}
```

</details>
