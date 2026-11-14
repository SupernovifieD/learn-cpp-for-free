// expect-fail: a void function gives no value to store
#include <iostream>

void printBanner()
{
    std::cout << "*** Welcome ***\n";
}

int main()
{
    int banner{printBanner()};
    std::cout << banner << "\n";
    return 0;
}
