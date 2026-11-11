---
description: Install a C++ compiler and a code editor or IDE on Windows, macOS or Linux, and check that your setup works before you write any code.
---

# 0.6 Installing an Integrated Development Environment (IDE)

To build programs, you need two things on your computer: a compiler and a place to write code. This lesson helps you install both on Windows, macOS or Linux, and then checks that they work. Setting up tools is rarely the fun part of programming, so take it one step at a time.

## What an IDE bundles, and what it does not

An **integrated development environment**, or IDE, combines a code editor, a way to build and run your program, and a debugger. Lesson 0.4 described these features, and they save a lot of time once you are writing real programs.

An IDE is not the compiler, though. On Windows, Visual Studio installs Microsoft's compiler for you, while editors such as Visual Studio Code need a compiler installed separately. On macOS and Linux you install the compiler yourself, whichever editor you choose.

You need only one setup, so choose the tab for your operating system. The tabs follow the same order: what to install, how to check it, and which editors work well.

## Installing your tools

=== "Windows"

    **Install:** The most direct choice is [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/), which is free for individual developers and for some other uses that its license terms list. Run its installer and, when it asks which workloads to install, select **Desktop development with C++**. This workload includes the Microsoft C++ compiler.

    Microsoft's guide to [installing C and C++ support in Visual Studio](https://learn.microsoft.com/en-us/cpp/build/vscpp-step-0-installation) walks through the same steps.

    **Check:** Open **Developer Command Prompt for Visual Studio** from the Start menu, then enter this command:

    ```powershell
    cl
    ```

    The compiler prints its name, its version and a short list of usage hints.

    **Editor:** Visual Studio is both the editor and the IDE. If you prefer Visual Studio Code, install it together with its C/C++ extension, and install a compiler separately: either the Microsoft compiler from Visual Studio or its Build Tools, or GCC through [MSYS2](https://www.msys2.org/). The official guides for [Microsoft C++](https://code.visualstudio.com/docs/cpp/config-msvc) and [MinGW-w64 with MSYS2](https://code.visualstudio.com/docs/cpp/config-mingw) list each step.

=== "macOS"

    **Install:** Apple's compiler, Clang, comes with the Xcode Command Line Tools. Open the **Terminal** app and enter:

    ```bash
    xcode-select --install
    ```

    A window asks you to confirm, and the download starts. You do not need the full Xcode application to follow this book.

    **Check:** Enter this command in the Terminal:

    ```bash
    clang++ --version
    ```

    It prints the compiler's name and version. The `g++` command on macOS is usually Apple's Clang under another name, so `g++ --version` shows the same compiler.

    **Editor:** Any code editor works. Popular choices are Visual Studio Code with its C/C++ extension, Xcode and CLion. JetBrains announced in 2025 that CLion is free for non-commercial use, so check its license page for the current terms before you rely on that. The official guide to [Clang on macOS with Visual Studio Code](https://code.visualstudio.com/docs/cpp/config-clang-mac) lists each step.

=== "Linux"

    **Install:** Install the GNU C++ compiler, `g++`, with your distribution's package manager. If you also want Clang, install it the same way.

    ```bash
    # Debian and Ubuntu
    sudo apt install build-essential
    sudo apt install clang

    # Fedora
    sudo dnf install gcc-c++
    sudo dnf install clang

    # Arch Linux
    sudo pacman -S gcc
    sudo pacman -S clang
    ```

    Package names can change, so check your distribution's documentation if a command fails. On Debian and Ubuntu, `build-essential` also installs `make` and other basic build tools.

    **Check:** Enter these commands in a terminal:

    ```bash
    g++ --version
    clang++ --version
    ```

    Each command prints the compiler's name and version. You only need the second command if you installed Clang.

    **Editor:** Any editor works, from a simple text editor to a full IDE. Visual Studio Code with its C/C++ extension is a common choice, and its [guide for Linux](https://code.visualstudio.com/docs/cpp/config-linux) lists each step.

## Is my compiler recent enough?

This book uses C++20, and the compiler you installed is probably recent enough. Compilers gained C++20 features gradually, so a very old compiler may lack some of them. If yours is more than a few years old, update it.

There is no single version number that means "complete C++20". The [C++20 compiler support table on cppreference](https://en.cppreference.com/w/cpp/compiler_support/20) lists each feature with the first version of GCC, Clang, MSVC and Apple Clang that supports it. The page is maintained on a best-effort basis, so treat it as a guide.

!!! tip
    Run the check command from your tab again after you install updates. The version number it prints is the quickest way to see what you have.

## Online compilers

If you only want to try a few lines of code, an online compiler needs no installation. [Compiler Explorer](https://godbolt.org/) is one example, and it also shows the assembly that your code turns into.

Online compilers have limits. They are awkward for programs made of several files, and they do not teach you the tools you will use for real projects. Treat them as a temporary option, and finish installing your own setup soon.

## Summary

- An IDE bundles an editor, build tools and a debugger, and it is not the compiler.
- On Windows, install Visual Studio Community with the **Desktop development with C++** workload, or use Visual Studio Code with a compiler of your choice.
- On macOS, install the Xcode Command Line Tools with `xcode-select --install`.
- On Linux, install `g++` with your package manager, and install Clang too if you want a second compiler.
- Check your installation with `cl` in a Developer Command Prompt, or with `g++ --version` or `clang++ --version`.
- Online compilers are fine for quick experiments, but they are no substitute for your own setup.

## Further reading

- [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/)
- [Install C and C++ support in Visual Studio](https://learn.microsoft.com/en-us/cpp/build/vscpp-step-0-installation)
- [Visual Studio Code: using Microsoft C++ on Windows](https://code.visualstudio.com/docs/cpp/config-msvc)
- [Visual Studio Code: using GCC with MinGW-w64](https://code.visualstudio.com/docs/cpp/config-mingw)
- [Visual Studio Code: using Clang on macOS](https://code.visualstudio.com/docs/cpp/config-clang-mac)
- [Visual Studio Code: using GCC on Linux](https://code.visualstudio.com/docs/cpp/config-linux)
- [C++ compiler support (cppreference)](https://en.cppreference.com/w/cpp/compiler_support)
