# 2. C++ Basics: Functions and Files

A program of any size is built from pieces. This chapter shows you how to write your own functions, how to pass values into them and get answers out, and how to spread a program over several files that share their declarations through headers. It also introduces the preprocessor and namespaces, and it ends with advice on how to design a program before you write it.

## What you will be able to do after this chapter

- Write functions that take values and return results, and call them from other functions.
- Explain where a name can be used in a program, and where it cannot.
- Split a program into several files and build them together.
- Share declarations between files with header files, and protect a header with a header guard.
- Use namespaces and the preprocessor's include and conditional directives.
- Plan a small program on paper before you write the first line.

## Lessons in this chapter

- [2.1 Introduction to functions](01-introduction-to-functions.md): defining a function and calling it.
- [2.2 Function return values](02-function-return-values.md): handing a value back to the caller, and what `main` returns.
- [2.3 Void functions (non-value returning functions)](03-void-functions.md): functions that do something and return nothing.
- [2.4 Introduction to function parameters and arguments](04-introduction-to-function-parameters-and-arguments.md): passing values into a function.
- [2.5 Introduction to local scope](05-introduction-to-local-scope.md): where a variable lives and where its name can be used.
- [2.6 Why functions are useful, and how to use them effectively](06-why-functions-are-useful-and-how-to-use-them-effectively.md): when to write a function, and how to keep it good.
- [2.7 Forward declarations and definitions](07-forward-declarations-and-definitions.md): calling a function before its definition, and the one-definition rule.
- [2.8 Programs with multiple code files](08-programs-with-multiple-code-files.md): building one program from several source files.
- [2.9 Naming collisions and an introduction to namespaces](09-naming-collisions-and-an-introduction-to-namespaces.md): keeping names apart, and why the book writes `std::`.
- [2.10 Introduction to the preprocessor](10-introduction-to-the-preprocessor.md): what happens before the compiler, macros and conditional compilation.
- [2.11 Header files](11-header-files.md): sharing declarations between files.
- [2.12 Header guards](12-header-guards.md): keeping a header from being used twice, and what guards cannot fix.
- [2.13 How to design your first programs](13-how-to-design-your-first-programs.md): planning a program, and building it one task at a time.
- [2.x Chapter 2 summary and quiz](x-summary-and-quiz.md): a recap of the chapter, and eight questions to test yourself.
