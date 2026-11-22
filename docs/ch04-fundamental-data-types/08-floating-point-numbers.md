# 4.8 Floating point numbers

An integer cannot hold 3.5 or 0.25, and many quantities need a fractional part: a price, a temperature, a distance. C++ stores such numbers in the floating point types. They are powerful, and they come with limits that surprise most beginners, so this lesson spends as much time on what they cannot do as on what they can.

## The floating point types

A **floating point** number is stored as a significand and an exponent, the two parts of scientific notation from [lesson 4.7](07-introduction-to-scientific-notation.md), written in binary. The name comes from the exponent: it moves, or floats, the point to where it belongs. C++ has three floating point types:

| Type | Size | Digits |
| --- | --- | --- |
| `float` | 4 bytes | 6 to 7 |
| `double` | 8 bytes | 15 to 16 |
| `long double` | varies | varies |

The sizes are the ones that you find on mainstream computers, where `float` and `double` follow the **IEEE 754** standard for floating point numbers. The last column says how many significant digits survive in the number. The third type, `long double`, has a different size and precision on different platforms, so the book names it and does not use it.

> [!BEST-PRACTICE]
> Use `double` for floating point values. It has far more precision than `float` for a small cost, and a `float` is worth considering only when a program stores a very large number of values and memory is tight.

## How far they reach

Floating point types reach far beyond the integers. On mainstream computers the largest `float` is about 3.4e38, and the largest `double` is about 1.8e308, which is a number with 309 digits. Nothing in the integer types comes close.

The reach has a price. The marks on the number line get farther apart as the numbers grow, so the precision is relative: a `double` is precise to about 16 digits whether the number is tiny or huge. A `float` counts every whole number up to 16,777,216, and above that it cannot tell 16,777,216 from 16,777,217. This is why an exact count, such as the number of seats in a theater, belongs in an integer type, and a measurement belongs in a floating point type.

## The f suffix

A literal such as `3.14` is a `double`. If you put it into a `float`, the value has to be rounded, because a `float` does not have enough digits to hold 3.14 exactly. The nearest `float` is 3.1400001, so the value changes slightly. The compiler warns about this, and the book's options turn the warning into an error:

```cpp title="float-literal.cpp"
{{#include ../../examples/ch04/08-float-literal.fail.cpp}}
```

The second line of the file says that the program builds without `-Werror`. This is not the narrowing error of [lesson 1.4](../ch01-cpp-basics/04-variable-assignment-and-initialization.md): the value 3.14 is within the range of a `float`, and the language allows the conversion. The complaint comes from the warning options, which are part of `-Wconversion`.

The cure is to say that the literal is a `float`. A literal with the suffix `f` has the type `float`, so `float ratio{3.14f};` builds without a warning. The book writes the suffix `f` in lower case.

## Precision and std::setprecision

A `double` holds about 16 significant digits, and `std::cout` shows six unless you ask for more. The manipulator `std::setprecision` from the header `<iomanip>` sets the number of significant digits. It stays in effect for every output that follows, until you set another value:

```cpp title="precision.cpp"
{{#include ../../examples/ch04/08-precision.cpp}}
```

```text title="Output"
{{#include ../../examples/ch04/08-precision.out}}
```

The first line uses the default of six digits. The next two lines ask for three and for twelve digits, and the last line shows that the setting of twelve is still active for another value. Notice that trailing zeros are not printed: the number needs no more digits than it has.

A `float` runs out of digits much sooner than a `double`. This program stores a third in each type, and prints each with a few digits more than the type can hold:

```cpp title="float-and-double.cpp"
{{#include ../../examples/ch04/08-float-and-double.cpp}}
```

```text title="Output"
{{#include ../../examples/ch04/08-float-and-double.out}}
```

Only the first seven digits of the `float` are meaningful, and the digits after them are the remains of the rounding. The `double` has twice as many good digits. The suffix `f` on `1.0f` and `3.0f` keeps the calculation in `float`.

## Rounding errors

Most decimal fractions cannot be stored exactly in binary. Think of a ruler whose marks are at a half, a quarter, an eighth and so on, because binary fractions are sums of powers of two. A value such as 0.5 or 0.25 sits exactly on a mark. A tenth does not, so the computer stores the nearest mark, in the same way that 0.333 is the nearest three-digit decimal to a third.

```cpp title="rounding-error.cpp"
{{#include ../../examples/ch04/08-rounding-error.cpp}}
```

```text title="Output"
{{#include ../../examples/ch04/08-rounding-error.out}}
```

With seventeen digits, the stored value of 0.1 turns out to be slightly more than a tenth, and the sum of 0.1 and 0.2 is not quite 0.3. With the default six digits you never see this, because the error is far below the sixth digit. The error is small, and it is also real.

> [!WARNING]
> Do not test two floating point values for exact equality after a calculation. Results that look equal on paper can differ in the last digit. [Lesson 4.9](09-boolean-values.md) shows the comparison operators, and a later chapter shows how to compare floating point values safely.

## Integer and floating point division

Division gives different results for integers and for floating point numbers. When both operands are integers, the result is an integer and the fraction is dropped, as [lesson 1.9](../ch01-cpp-basics/09-introduction-to-literals-and-operators.md) explained. When at least one operand is a floating point number, the result is a floating point number:

```cpp title="division.cpp"
{{#include ../../examples/ch04/08-division.cpp}}
```

```text title="Output"
{{#include ../../examples/ch04/08-division.out}}
```

In `7.0 / 2` the integer 2 is converted to the floating point number 2.0 before the division. To get a fraction, make one operand a floating point literal, and a later chapter explains the full rules for mixing types.

## Infinity and NaN

Two special values come with the floating point types: **infinity**, which is larger than any number, and **NaN**, short for "not a number", which is the result of a calculation without an answer. The C++ standard says that dividing by zero is undefined behavior, for floating point types as well as for integers. Computers that follow IEEE 754 define the result as infinity, or as NaN for 0.0 divided by 0.0, but the language itself does not promise it, and the text that `std::cout` prints for these values differs between platforms. The book shows no program for them, and you should avoid dividing by zero.

<details>
<summary>Check your understanding</summary>

**Question 1.** What does `std::cout << 9 / 2.0;` print?

<details>
<summary>Answer</summary>

It prints `4.5`. One operand is a floating point number, so the division is a floating point division and keeps the fraction.

</details>

**Question 2.** Why does `float ratio{3.14};` fail to build with the book's options, and how do you fix it?

<details>
<summary>Answer</summary>

The literal `3.14` is a `double`, and storing it in a `float` changes its value to the nearest `float`. The compiler warns about the change, and `-Werror` makes the warning an error. Write `float ratio{3.14f};`.

</details>

**Question 3.** Why is the sum of 0.1 and 0.2 not exactly 0.3 in a program?

<details>
<summary>Answer</summary>

Neither 0.1 nor 0.2 can be stored exactly in binary, so each is the nearest value that the type can hold, and the sum of the two stored values is a little different from the nearest value to 0.3.

</details>

</details>

## Summary

- The floating point types are `float`, `double` and `long double`, and the book uses `double`.
- A `double` literal such as `3.14` needs the suffix `f` to become a `float`, and the book's options reject the conversion without it.
- `std::cout` prints six significant digits, and `std::setprecision` from `<iomanip>` changes that until the next call.
- Most decimal fractions are stored with a small rounding error, so do not compare floating point values for exact equality.
- Integer division drops the fraction, and a division with a floating point operand keeps it.
- Dividing by zero is undefined behavior, even though IEEE 754 platforms give infinity or NaN.

## Further reading

- [Fundamental types: floating point types (cppreference)](https://en.cppreference.com/w/cpp/language/types)
- [std::setprecision (cppreference)](https://en.cppreference.com/w/cpp/io/manip/setprecision)
- [std::numeric_limits::is_iec559 (cppreference)](https://en.cppreference.com/w/cpp/types/numeric_limits/is_iec559)
