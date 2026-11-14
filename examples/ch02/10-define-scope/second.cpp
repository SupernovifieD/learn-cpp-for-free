#include <iostream>

void printSecond()
{
#ifdef SHOW_MARKER
    std::cout << "second.cpp: SHOW_MARKER is defined\n";
#endif
#ifndef SHOW_MARKER
    std::cout << "second.cpp: SHOW_MARKER is not defined\n";
#endif
}
