#include "sum.h"

#include <iostream>

int main()
{
    int first{};
    int second{};
    std::cout << "First: ";
    std::cin >> first;
    std::cout << "Second: ";
    std::cin >> second;
    std::cout << "Sum: " << sum(first, second) << "\n";
    return 0;
}
