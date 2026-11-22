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
