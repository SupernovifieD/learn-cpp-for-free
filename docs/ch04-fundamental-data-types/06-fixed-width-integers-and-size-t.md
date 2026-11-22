# 4.6 Fixed-width integers and size_t

The size of an `int` is not the same on every computer, and the size of a `long` differs even between mainstream platforms. For most programs that does not matter. When it does, because a value must have exactly 32 bits or a counter must reach beyond two billion, C++ offers types whose names state the size. This lesson introduces them, a surprise that comes with the smallest ones, and the type that `sizeof` returns.

## Why the size of int varies

[Lesson 4.3](03-object-sizes-and-the-sizeof-operator.md) showed that the standard only sets minimums. An `int` must have at least 16 bits, and mainstream computers use 32. A `long` must have at least 32 bits, and it has 32 on 64-bit Windows and 64 on 64-bit macOS and Linux.

The language leaves the size of `int` open on purpose, so that it can match what each computer handles best. A program that quietly depends on one of these sizes works on the computer where it was written and may fail on another.

The fix is to ask for the size you need by name, so that the program says what it means.

## The fixed-width types

The header `<cstdint>` defines integer types with an exact number of bits. Their names contain that number, and they belong to the `std` namespace, which [lesson 2.9](../ch02-functions-and-files/09-naming-collisions-and-an-introduction-to-namespaces.md) introduced. The `_t` at the end is the suffix from [lesson 4.1](01-introduction-to-fundamental-data-types.md). The eight names are:

- **Signed:** `std::int8_t`, `std::int16_t`, `std::int32_t` and `std::int64_t`.
- **Unsigned:** `std::uint8_t`, `std::uint16_t`, `std::uint32_t` and `std::uint64_t`.

This program uses three of them, and prints their sizes together with the size of an `int`:

```cpp title="fixed-widths.cpp"
{{#include ../../examples/ch04/06-fixed-widths.cpp}}
```

```text title="Output"
{{#include ../../examples/ch04/06-fixed-widths.out}}
```

The ranges follow from the bit counts, with the tables of lessons [4.4](04-signed-integers.md) and [4.5](05-unsigned-integers-and-why-to-avoid-them.md): `std::int32_t` holds -2,147,483,648 to 2,147,483,647, and `std::uint16_t` holds 0 to 65,535. Each type has exactly the size that its name says: `std::int16_t` has 2 bytes, `std::int32_t` has 4, and `std::int64_t` has 8. The value 9,000,000,000 would not fit in 32 bits, so the program needs a 64-bit type for it, and `std::int64_t` says so without depending on the size of `long`. The line for `int` shows 4 bytes on the platforms of this book, but only the fixed-width types promise a size.

The exact-width types are optional in theory: a platform provides one only if it has an integer type of exactly that size. Every mainstream platform provides all eight, so you can use them freely.

The header also defines two other families. A name such as `std::int_fast32_t` is the fastest type with at least 32 bits, and `std::int_least32_t` is the smallest type with at least 32 bits. Both always exist, and most programs never need them.

## The smallest types print as characters

The types `std::int8_t` and `std::uint8_t` hold a number from a tiny range, and on the mainstream compilers they are names for `signed char` and `unsigned char`. These are character types, which [lesson 4.11](11-chars.md) introduces, and `std::cout` prints a character type as a character:

```cpp title="small-ints.cpp"
{{#include ../../examples/ch04/06-small-ints.cpp}}
```

```text title="Output"
{{#include ../../examples/ch04/06-small-ints.out}}
```

The values 65 and 66 are the codes of the letters `A` and `B`, so the program prints letters and not numbers. The value is right, and only the way of printing is surprising. [Lesson 4.12](12-introduction-to-type-conversion-and-static-cast.md) shows how to print the number: convert the value to `int` with `static_cast` first.

## When to use which

> [!BEST-PRACTICE]
> Use `int` for everyday quantities, and a fixed-width type when the exact size is part of what the value means. Examples are a field of a file format, a value that a device defines, and a count that can grow beyond two billion, for which `std::int64_t` is the clear choice.

The reason is clarity. When you write `std::int32_t`, a reader knows that the size matters, and the program has the same meaning on every platform. When you write `int`, you say that the size is of no importance, which is true for most variables.

## The size_t type

The result of `sizeof` has the type **`std::size_t`**. It is an unsigned integer type that is large enough for the size of the largest object that the platform allows. That makes it 8 bytes on a 64-bit platform, as the last line of the output above shows, and 4 bytes on a 32-bit platform.

The standard library uses `std::size_t` for sizes and counts, such as the number of characters in a string, which lesson 5.7 introduces. The type is defined in the header `<cstddef>`, and the program above includes it. A variable that holds the result of `sizeof` has this type:

```cpp
std::size_t intSize{sizeof(int)};
```

An unsigned type brings the problems of [lesson 4.5](05-unsigned-integers-and-why-to-avoid-them.md), so use `std::size_t` for what the library gives you, and signed types for your own quantities.

<details>
<summary>Check your understanding</summary>

**Question 1.** What does this program print?

```cpp
std::uint8_t code{67};
std::cout << code;
```

<details>
<summary>Answer</summary>

It prints `C`. A `std::uint8_t` is usually a character type, and 67 is the code of the letter C, so `std::cout` prints the letter.

</details>

**Question 2.** A counter must hold values up to 5,000,000,000 on every platform. Which type should it have, and why not `long`?

<details>
<summary>Answer</summary>

`std::int64_t`. A `long` has only 32 bits on 64-bit Windows, which is too small for the value, while `std::int64_t` has 64 bits on every platform that provides it.

</details>

**Question 3.** Which type does `sizeof(double)` have?

<details>
<summary>Answer</summary>

`std::size_t`, an unsigned integer type that is large enough to hold the size of any object.

</details>

</details>

## Summary

- The size of `int` and `long` varies between platforms, and the standard only sets minimums.
- The header `<cstdint>` defines types with an exact size, such as `std::int32_t` and `std::uint64_t`, and every mainstream platform provides them.
- `std::int8_t` and `std::uint8_t` are usually character types, so `std::cout` prints them as characters.
- Use `int` for everyday quantities, and a fixed-width type when the exact size is part of the meaning.
- `std::size_t` is the unsigned type that `sizeof` returns, and the library uses it for sizes and counts.

## Further reading

- [Fixed-width integer types (cppreference)](https://en.cppreference.com/w/cpp/types/integer)
- [std::size_t (cppreference)](https://en.cppreference.com/w/cpp/types/size_t)
