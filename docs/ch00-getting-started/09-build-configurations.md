# 0.9 Configuring your compiler: Build configurations

The same source code can be compiled in different ways, and the way you choose changes how the program behaves while you work on it. This lesson explains build configurations, compares the two you will meet most often, and recommends one for learning. The next three lessons then show how to configure your compiler for the best learning experience.

## What a build configuration is

A **build configuration** is a named set of settings for the compiler and the linker. Choosing a configuration tells your tools how to build the program, and the source code stays exactly the same.

Most IDEs create two configurations for every new project, called **Debug** and **Release**. Compilers on the command line have no named configurations, but you get the same effect by passing different options.

## Debug and release

A debug build is meant for the time when you are writing and fixing a program. A release build is meant for the program you give to other people, or the one you use to measure how fast your code is.

| Aspect | Debug | Release |
| --- | --- | --- |
| Optimization | Off, so the compiled code follows your source closely | On, so the compiler rearranges and shortens the code |
| Debug information | Included, so a debugger can show your lines and names | Usually left out, or stored in a separate file |
| Assertions | Enabled | Disabled |
| Speed | Slower | Faster |
| Size | Usually larger | Usually smaller |
| Ease of debugging | Higher, because the program runs the way you wrote it | Lower, because the optimizer changes the order and shape of the code |

An **assertion** is a check that stops the program with a message when something that should always be true turns out to be false. In C++, the `assert` tool of the Standard Library does nothing when a macro named `NDEBUG` is defined, and release builds usually define it.

## Switching configurations

{{#tabs}}
{{#tab Visual Studio}}

**Switch:** In the toolbar, open the **Solution Configurations** list and choose **Debug** or **Release**. You can also open the **Build** menu, choose **Configuration Manager** and pick a configuration there.

**Effect:** The Debug configuration keeps the optimizer off and produces debug information. The Release configuration is fully optimized, so it is not meant for stepping through your code line by line.

{{#endtab}}
{{#tab VS Code}}

**Switch:** Visual Studio Code has no Debug and Release switch of its own. Your build task decides, so you choose a configuration by changing the options that the task passes to the compiler. The official guides linked in lesson 0.6 show where those options live.

**Effect:** Use the options from the **Command line** tab: the debug options for everyday work, and the release options when you want a fast build.

{{#endtab}}
{{#tab Command line}}

**Switch:** With GCC or Clang, `-O0` turns optimization off, `-g` adds debug information, `-O2` turns on a high level of optimization and `-DNDEBUG` defines the `NDEBUG` macro.

```bash
# Debug build
g++ -std=c++20 -O0 -g -o hello-world hello-world.cpp

# Release build
g++ -std=c++20 -O2 -DNDEBUG -o hello-world hello-world.cpp
```

With Microsoft's compiler, `/Od` turns optimization off, `/Zi` produces debug information, `/O2` optimizes for speed and `/DNDEBUG` defines the macro.

```powershell
cl /std:c++20 /EHsc /Od /Zi /Fe:hello-world.exe hello-world.cpp
cl /std:c++20 /EHsc /O2 /DNDEBUG /Fe:hello-world.exe hello-world.cpp
```

**Effect:** The first command in each block builds a debug version and the second builds a release version.

{{#endtab}}
{{#endtabs}}

## Which one to use

While you are learning, use the debug configuration. Programs in debug builds behave the way your code reads, debuggers can show you what is happening, and the compiler builds quickly. Use a release configuration when you are ready to hand a program to someone else, and when you want to measure how fast it really runs, because speed in a debug build does not tell you anything useful.

> [!BEST-PRACTICE]
> Develop and test in a debug configuration, and measure performance only in a release configuration.

The settings in the next lessons, such as warning levels and language standards, should apply to every configuration. In Visual Studio, open the project's property pages and choose **All Configurations** in the **Configuration** list before you change a setting, so that Debug and Release stay in step.

## Summary

- A build configuration is a named set of compiler and linker settings, and the source code does not change.
- Debug builds have no optimization, include debug information and keep assertions, so they are easier to debug but slower.
- Release builds are optimized, usually leave out debug information and disable assertions, so they run faster.
- Visual Studio switches with the **Solution Configurations** list, and on the command line you switch with options such as `-O0 -g` and `-O2 -DNDEBUG`.
- Use a debug configuration while you learn, and apply the settings from the next lessons to all configurations.

## Further reading

- [GCC documentation: optimization options](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)
- [GCC documentation: debugging options](https://gcc.gnu.org/onlinedocs/gcc/Debugging-Options.html)
- [Microsoft documentation: debug and release configurations](https://learn.microsoft.com/en-us/visualstudio/debugger/how-to-set-debug-and-release-configurations)
- [Microsoft documentation: /Od (disable optimization)](https://learn.microsoft.com/en-us/cpp/build/reference/od-disable-debug)
- [cppreference: assert](https://en.cppreference.com/w/cpp/error/assert)
