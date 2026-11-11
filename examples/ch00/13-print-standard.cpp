#include <iostream>

int main()
{
#if defined(_MSVC_LANG)
    // Microsoft's compiler keeps __cplusplus at 199711L unless /Zc:__cplusplus
    // is given, so ask _MSVC_LANG instead.
    const long standard{_MSVC_LANG};
#else
    const long standard{__cplusplus};
#endif

    std::cout << "Language standard value: " << standard << "\n";

    if (standard >= 202302L)
    {
        std::cout << "C++23 or newer\n";
    }
    else if (standard >= 202002L)
    {
        std::cout << "C++20\n";
    }
    else if (standard >= 201703L)
    {
        std::cout << "C++17\n";
    }
    else if (standard >= 201402L)
    {
        std::cout << "C++14\n";
    }
    else if (standard >= 201103L)
    {
        std::cout << "C++11\n";
    }
    else
    {
        std::cout << "C++98 or C++03\n";
    }

    return 0;
}
