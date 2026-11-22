# 4. Fundamental Data Types

Every value in a program has a type, and the type decides what the value can be, how much memory it takes and what you can do with it. So far you have used `int` almost everywhere. This chapter introduces the rest of the types that C++ builds in: whole numbers of several sizes, numbers with a fractional part, yes-or-no values and characters. Along the way it teaches the first statement that lets a program choose, `if`, and how to convert a value from one type to another on purpose.

## What you will be able to do after this chapter

- Choose a type for a quantity, and say how its size limits the values it can hold.
- Predict what signed and unsigned integers do at the edge of their range, and choose the type that avoids surprises.
- Write numbers with a fractional part, including scientific notation, and explain why they are not always exact.
- Use `bool`, the comparison operators and `if`, `else` and `else if` to make a program choose between actions.
- Read, print and calculate with characters.
- Convert a value from one type to another on purpose with `static_cast`.

## Lessons in this chapter

- [4.1 Introduction to fundamental data types](01-introduction-to-fundamental-data-types.md): bits, types and the map of the built-in types.
- [4.2 Void](02-void.md): the type that stands for no value.
- [4.3 Object sizes and the sizeof operator](03-object-sizes-and-the-sizeof-operator.md): how the size of a type limits its values, and how to ask for it.
- [4.4 Signed integers](04-signed-integers.md): the signed types, their ranges, and what overflow does.
- [4.5 Unsigned integers, and why to avoid them](05-unsigned-integers-and-why-to-avoid-them.md): wraparound, mixing signs, and a preference for signed types.
- [4.6 Fixed-width integers and size_t](06-fixed-width-integers-and-size-t.md): types with an exact size, and the type that sizeof returns.
- [4.7 Introduction to scientific notation](07-introduction-to-scientific-notation.md): significand and exponent, and E-notation in C++ literals.
- [4.8 Floating point numbers](08-floating-point-numbers.md): float and double, precision, rounding errors and division.
- [4.9 Boolean values](09-boolean-values.md): true and false, comparisons, and reading and printing a bool.
- [4.10 Introduction to if statements](10-introduction-to-if-statements.md): if, else and else if, and the mistake of writing = for ==.
- [4.11 Chars](11-chars.md): characters as codes, reading a char, escape sequences and quotes.
- [4.12 Introduction to type conversion and static_cast](12-introduction-to-type-conversion-and-static-cast.md): implicit conversions, why risky ones are rejected, and converting on purpose.
- [4.x Chapter 4 summary and quiz](x-summary-and-quiz.md): a recap of the chapter, and eight questions to test yourself.
