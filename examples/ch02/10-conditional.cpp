#include <iostream>

#define SHOW_EXTRA

int main()
{
    std::cout << "always printed\n";

#ifdef SHOW_EXTRA
    std::cout << "SHOW_EXTRA is defined\n";
#endif

#ifndef SHOW_EXTRA
    std::cout << "SHOW_EXTRA is not defined\n";
#endif

#if 0
    std::cout << "switched off with #if 0\n";
#endif

    return 0;
}
