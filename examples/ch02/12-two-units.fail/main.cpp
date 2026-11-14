// expect-fail: both source files get a definition from units.h
#include <iostream>

int firstMinutes();
int secondMinutes();

int main()
{
    std::cout << firstMinutes() << " " << secondMinutes() << "\n";
    return 0;
}
