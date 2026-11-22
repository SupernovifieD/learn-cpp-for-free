// expect-fail: the name totl is used but only total is declared
#include <iostream>

int main()
{
    int total{12};
    std::cout << "Total: " << total << "\n";
    std::cout << "Half: " << totl / 2 << "\n";
    return 0;
}
