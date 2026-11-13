# 0.2 Introduction to programs and programming languages

Before you write programs, it helps to know what a program is and how a computer carries one out. This lesson follows the path from the hardware inside the machine, through the languages used to instruct it, to the place C++ occupies among them. You do not need to memorize anything here. The goal is a mental picture that later lessons can build on.

## What a program is

A **program** is a sequence of instructions that a computer carries out, one after another, to complete a task. A recipe is a reasonable comparison, with one big difference: a cook can guess what "season to taste" means, but a computer does exactly what the instructions say, and nothing else.

The computer's physical parts are called **hardware**. The programs it runs, together with the data they use, are called **software**.

## A quick tour of the hardware

Four kinds of hardware matter for understanding programs:

- The **CPU** (central processing unit) carries out instructions. It does arithmetic, compares values and decides which instruction to run next.
- **Memory**, often called RAM, is the fast working space that holds the programs and data in use right now. Its contents disappear when the power goes off.
- **Storage**, such as a solid-state drive, keeps files and programs for the long term. It is slower than memory, but it remembers everything when the power is off.
- **Input and output devices** connect the computer to the world. A keyboard, a mouse and a microphone are input devices, while a screen and speakers are output devices.

A program lives in storage. When you start it, the computer copies it into memory, and the CPU reads its instructions from there, one at a time.

> [!KEY-INSIGHT]
> A CPU does not understand your ideas. It understands a small, fixed set of very simple instructions, such as adding two numbers, comparing them or jumping to a different instruction. Every program you will ever run is built from instructions like these.

## Machine language

The instructions a CPU understands are written as patterns of bits, which are ones and zeros. Together they form the CPU's **machine language**. The design of that language, meaning which instructions exist and how they are encoded, is the CPU's **instruction set architecture**, or **ISA**.

Different families of CPUs use different ISAs. Two common ones are x86-64, which many desktop and laptop computers use, and ARM64, which phones and many recent laptops use. A program written in the machine language of one ISA cannot run directly on a CPU that uses another.

Here is a function that adds two whole numbers, written in the machine language of x86-64. It is only five bytes long, and in hexadecimal they are `89 F8 01 F0 C3`.

The exact bytes depend on the ISA, the compiler and its settings, so treat this as an illustration rather than something to remember. Nobody writes programs this way by choice, because the numbers say nothing about what they mean.

## Assembly language

**Assembly language** gives each machine instruction a short, readable name. A tool called an **assembler** translates the names back into machine code. The five bytes above are three instructions, and in assembly they look like this:

```x86asm title="x86-64 assembly (illustrative)"
mov eax, edi   ; eax = first
add eax, esi   ; eax += second
ret            ; return eax
```

A **register** is a tiny storage location inside the CPU. The first line copies the first number into a register named `eax`, the second line adds the other number to it, and the third line returns to the caller with the sum still in `eax`. The bytes `89 F8` are the first line, `01 F0` is the second and `C3` is the third.

Assembly is easier to read than raw numbers, but it is still tied to one ISA. This is the same job on ARM64, and the instructions and registers are different:

```armasm title="ARM64 assembly (illustrative)"
add w0, w1, w0
ret
```

Real compilers often choose different instructions for the same job, so what you see in your own tools will not match these lines exactly.

## High-level languages

Writing whole programs in assembly would be slow and error-prone, and the result could run on only one family of CPUs. A **high-level language** solves both problems. It lets you describe what you want using names, arithmetic and structure that resemble human reasoning, and it leaves the choice of instructions to a tool.

This is the same addition in C++. You do not need to understand it yet. The function returns the sum of its two parameters:

```cpp
int add(int a, int b)
{
    return a + b;
}
```

Something has to translate high-level code into machine language, and there are two main approaches. A **compiler** translates a whole program before it runs and produces a file of machine code. An **interpreter** reads a program while it runs and carries out each step as it goes.

| Aspect | Compiler | Interpreter |
| --- | --- | --- |
| When translation happens | Before the program runs | While the program runs |
| What the CPU runs | The machine code the compiler produced | The interpreter itself, which reads your code |
| Typical speed at run time | Usually faster | Usually slower |
| Typical benefit | Speed, and many mistakes found early | Quick to try, and no separate build step |

The line between the two is blurry. Many language implementations mix the approaches, and a **just-in-time (JIT) compiler**, for example, translates parts of a program into machine code while the program is already running.

> [!TIP]
> You can look at real assembly yourself. [Compiler Explorer](https://godbolt.org/) is a website where you type C++ and see what different compilers produce for it.

## Portability

A program is **portable** when it can run on different kinds of computers with little or no change. Machine code and assembly are not portable, because they belong to one ISA. High-level source code can be portable, because you can give the same source to a separate compiler for each kind of computer.

Portability has limits. Code that talks to one operating system's features, to particular graphics hardware or to a specific device has to be written differently for each target, so platform-specific code still exists in most large programs.

## Where C++ fits

C++ is a compiled, high-level language that also lets you work close to the hardware. You write source code, a compiler translates it into machine code for your CPU, and the result runs directly, with no interpreter in between. That combination is why C++ is used when speed and control matter.

Lesson 0.3 looks at where C++ came from, and lesson 0.5 shows how your source code becomes a program.

<details>
<summary>Check your understanding</summary>

Why can't you copy a program built for an ARM64 phone onto an x86-64 laptop and run it?

<details>
<summary>Answer</summary>

The program contains machine code for ARM64, and an x86-64 CPU does not understand those instructions. You would need to build the source code again with a compiler that targets x86-64.

</details>

</details>

## Summary

- A program is a sequence of instructions, and a computer follows them exactly.
- The CPU runs instructions, memory holds what is in use, storage keeps files, and input and output devices connect to the world.
- Machine language is the set of bit patterns a CPU understands, and each family of CPUs has its own instruction set architecture.
- Assembly language gives machine instructions readable names but is still tied to one ISA.
- High-level languages are more readable and can be portable, and a compiler or an interpreter translates them into machine instructions.
- C++ is a compiled, high-level language that still gives you access to low-level details.
