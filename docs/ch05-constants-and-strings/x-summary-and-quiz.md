# 5.x Chapter 5 summary and quiz

This page recaps the lessons of Chapter 5 and then tests what you remember. The summary names the key terms of each lesson, so use it to find a lesson that you want to read again.

The quiz has eight questions in rising difficulty: the first three are about ideas, the next two are about reading and repairing programs, and the last three ask you to write a program. Try each question before you open its solution.

## Summary

- [5.1 Constant variables (named constants)](01-constant-variables-named-constants.md): `const` makes a variable that cannot change, and it must be initialized. A named constant replaces a magic number and is better than a macro.
- [5.2 Literals](02-literals.md): every literal has a type that comes from its spelling, and suffixes such as `u`, `LL` and `f` change it. A string literal ends in a null terminator, and `1 / 2` is 0.
- [5.3 Numeral systems (decimal, binary, hexadecimal, and octal)](03-numeral-systems.md): `0b`, `0x` and a leading `0` start binary, hexadecimal and octal literals, and `010` is 8. `std::hex`, `std::oct`, `std::dec` and `std::bitset` print in each base.
- [5.4 The as-if rule and compile-time optimization](04-the-as-if-rule-and-compile-time-optimization.md): the compiler may change anything that does not change observable behavior. Constant folding may happen at compile time, but the language does not promise it.
- [5.5 Constant expressions](05-constant-expressions.md): a constant expression must be evaluated at compile time where the language requires one. Literals, operators on them and `const` integers set from them qualify, and the size of a `std::bitset` requires one.
- [5.6 Constexpr variables](06-constexpr-variables.md): `constexpr` requires a constant initializer and implies `const`. Use it for values known when building, and `const` for values set while running.
- [5.7 Introduction to std::string](07-introduction-to-std-string.md): `std::string` owns its text, `>>` stops at whitespace, and `std::getline` with `std::ws` reads a whole line. `+` joins strings, and a copy copies the characters.
- [5.8 Introduction to std::string_view](08-introduction-to-std-string-view.md): a `std::string_view` is a read-only view of text that someone else owns. Use it for read-only parameters, and ask explicitly for a `std::string`.
- [5.9 std::string_view (part 2)](09-std-string-view-part-2.md): the owner must outlive its views, and a view of a temporary or of a returned local string dangles. `remove_prefix` and `remove_suffix` change only the view.

## Quiz

### Question 1

Choose `const` or `constexpr` for each constant.

- (a) The price of a pitch per night, which is 25.
- (b) The number of guests that the reader types, which must not change afterwards.
- (c) The total number of seats, calculated from the number of rows and the seats per row, which are both literals.
- (d) The result of calling a function with a value that was read from input.

<details>
<summary>Solution</summary>

- (a) `constexpr`, because the value is a literal that is known when the program is built.
- (b) `const`, because the value is set while the program runs.
- (c) `constexpr`, because it is calculated from constant expressions.
- (d) `const`, because a call with run-time data cannot be known at build time.

</details>

### Question 2

What is the type of each literal: `7`, `7u`, `7LL`, `7.0`, `7.0f`, `'7'` and `"7"`? What does `sizeof("7")` give, and why?

<details>
<summary>Solution</summary>

The types are `int`, `unsigned int`, `long long`, `double`, `float`, `char` and `const char[2]`. The size of `"7"` is 2: one byte for the character 7 and one for the null terminator that every string literal ends with.

</details>

### Question 3

Convert the binary literal `0b1011'0110` to decimal and to hexadecimal, and convert `0x2A` to binary.

<details>
<summary>Solution</summary>

The binary number 10110110 has a 1 in the positions worth 128, 32, 16, 4 and 2, so it is 182. Split into groups of four bits, 1011 is B and 0110 is 6, so the hexadecimal literal is `0xB6`. The hexadecimal number 2A is the groups 0010 and 1010, so it is `0b0010'1010`, which is 42.

</details>

### Question 4

One line of this program does not build. Find it and say why.

```cpp title="which-line.cpp"
{{#include ../../examples/ch05/x-q4-which-line.fail.cpp}}
```

<details>
<summary>Solution</summary>

The line `std::bitset<copy> second{};` does not build. The variable `cells` is a constant expression, because it is `const` and is set from `rows * 4`, and `rows` is `constexpr`. The variable `copy` is also `const`, but it is set from `typed`, a variable that can change, so its value is not known until run time.

The size of a `std::bitset` has to be a constant expression, so `copy` does not qualify. A constant initializer would fix it, as in `constexpr std::size_t copy{5};`.

</details>

### Question 5

This program should print the reminder, and the sanitizers report a problem. Find the mistake and fix it.

```cpp title="dangling.cpp"
{{#include ../../examples/ch05/x-q5-dangling.ub.cpp}}
```

<details>
<summary>Solution</summary>

The view `note` looks at the characters of `text`, and `text` is destroyed at the closing brace of the inner block, so `note` dangles when the program prints it. The text is long enough to be stored in memory that the string allocates, and the string releases that memory when it is destroyed.

The viewer outlived its owner. When the text has to survive the block, let a `std::string` keep a copy, so that the variable owns its characters:

```cpp title="dangling-fixed.cpp"
{{#include ../../examples/ch05/x-q5-dangling-fixed.cpp}}
```

```text title="Output"
{{#include ../../examples/ch05/x-q5-dangling-fixed.out}}
```

</details>

### Question 6

Write a program that asks for the number of guests and then for the name of the trip, which may contain spaces. It prints the trip and the guests in one line. Type 4 and `Lake weekend` when you test it.

<details>
<summary>Solution</summary>

The number is read with `>>`, so a line break stays in the input. `std::getline` with `std::ws` skips it and then reads the whole name, spaces included.

```cpp title="trip-name.cpp"
{{#include ../../examples/ch05/x-q6-trip-name.cpp}}
```

```text title="Example session"
{{#include ../../examples/ch05/x-q6-trip-name.session}}
```

</details>

### Question 7

Write a function `printLine` that takes a label and a value, both as read-only text, and prints them as `label: value`. Call it with a `std::string` and with a string literal.

<details>
<summary>Solution</summary>

Both parameters are `std::string_view`, so the function accepts the string and the literal without copying either of them.

```cpp title="print-line.cpp"
{{#include ../../examples/ch05/x-q7-print-line.cpp}}
```

```text title="Output"
{{#include ../../examples/ch05/x-q7-print-line.out}}
```

</details>

### Question 8

Write a program that prints the number 77 in decimal, in hexadecimal, in octal and in binary with 8 bits.

<details>
<summary>Solution</summary>

The program prints the value in decimal first, and then switches the base with `std::hex` and `std::oct`. The binary form comes from `std::bitset<8>`. The value 77 is `4d` in hexadecimal, `115` in octal and `01001101` in binary.

```cpp title="bases.cpp"
{{#include ../../examples/ch05/x-q8-bases.cpp}}
```

```text title="Output"
{{#include ../../examples/ch05/x-q8-bases.out}}
```

</details>
