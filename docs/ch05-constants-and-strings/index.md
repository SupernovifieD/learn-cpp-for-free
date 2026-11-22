# 5. Constants and Strings

Some values never change while a program runs, and some of the most useful values are not numbers at all. This chapter shows how to protect a value with `const` and `constexpr`, what the literals in your code really are, and how to write numbers in binary, hexadecimal and octal. It also explains the rule that lets a compiler optimize your program, and it introduces the two types that C++ offers for text: `std::string`, which owns its characters, and `std::string_view`, which only looks at them.

## What you will be able to do after this chapter

- Replace magic numbers with named constants, and choose between `const` and `constexpr`.
- Say what type a literal has, and use suffixes to choose it.
- Read and write numbers in binary, octal and hexadecimal, and print a value in each of them.
- Explain what the as-if rule allows a compiler to do, and what a constant expression is.
- Store, read and join text with `std::string`, including a line that has spaces in it.
- Pass text to a function with `std::string_view`, and avoid a view that outlives its string.

## Lessons in this chapter

- [5.1 Constant variables (named constants)](01-constant-variables-named-constants.md): magic numbers, `const`, and why a named constant beats a macro.
- [5.2 Literals](02-literals.md): the type of every literal, suffixes, and why `1 / 2` is 0.
- [5.3 Numeral systems (decimal, binary, hexadecimal, and octal)](03-numeral-systems.md): converting by hand, writing literals and printing in each base.
- [5.4 The as-if rule and compile-time optimization](04-the-as-if-rule-and-compile-time-optimization.md): what a compiler may change, and why compile-time work is not guaranteed.
- [5.5 Constant expressions](05-constant-expressions.md): values that are known when the program is built, and where the language requires them.
- [5.6 Constexpr variables](06-constexpr-variables.md): `constexpr`, and when to choose it over `const`.
- [5.7 Introduction to std::string](07-introduction-to-std-string.md): storing, reading and joining text, and reading a whole line.
- [5.8 Introduction to std::string_view](08-introduction-to-std-string-view.md): a read-only view of text, without copying it.
- [5.9 std::string_view (part 2)](09-std-string-view-part-2.md): owners and viewers, and the views that dangle.
