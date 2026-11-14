#include <iostream>

#define SHOW_MARKER

void printFirst()
{
#ifdef SHOW_MARKER
    std::cout << "first.cpp: SHOW_MARKER is defined\n";
#endif
#ifndef SHOW_MARKER
    std::cout << "first.cpp: SHOW_MARKER is not defined\n";
#endif
}
