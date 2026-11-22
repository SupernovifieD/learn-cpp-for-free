# 3. Debugging C++ Programs

Sooner or later every program does something its author did not intend, and the skill that separates a frustrated beginner from a confident one is knowing what to do next. This chapter sorts mistakes into kinds, lays out a procedure and a search strategy for finding them, and then moves from print statements to the tool that professionals reach for first: the debugger. It ends with the habits and tools that catch problems before they become bugs.

## What you will be able to do after this chapter

- Tell a syntax error, a semantic error and a logic error apart, and say who can notice each.
- Follow the debugging process and narrow a bug down to the function that causes it.
- Print debug messages to the error stream, and switch them on and off with the preprocessor.
- Step through a program, set breakpoints, watch variables and read the call stack in a debugger.
- Use warnings, static analysis, tests and sanitizers to find problems earlier.

## Lessons in this chapter

- [3.1 Syntax and semantic errors](01-syntax-and-semantic-errors.md): the kinds of mistakes, and which of them the compiler can find.
- [3.2 The debugging process](02-the-debugging-process.md): six steps from the first failure to a repaired program.
- [3.3 A strategy for debugging](03-a-strategy-for-debugging.md): reading, gathering evidence, and narrowing a bug down by halves.
- [3.4 Basic debugging tactics](04-basic-debugging-tactics.md): switching code off, tracing calls and printing values to the error stream.
- [3.5 More debugging tactics](05-more-debugging-tactics.md): debug output that a macro switches on and off, and logging.
- [3.6 Using an integrated debugger: Stepping](06-using-an-integrated-debugger-stepping.md): pausing a program and moving through it one statement at a time.
- [3.7 Using an integrated debugger: Running and breakpoints](07-using-an-integrated-debugger-running-and-breakpoints.md): running to a place, and breakpoints that stay.
