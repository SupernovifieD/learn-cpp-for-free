// expect-fail: two files define a function named pick
#include <iostream>

int pick();

int main()
{
    std::cout << "picked " << pick() << "\n";
    return 0;
}
