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
