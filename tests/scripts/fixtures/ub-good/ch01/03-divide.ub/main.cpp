// undefined-behavior: dividing by zero is undefined
#include "divide.h"

#include <iostream>

int main()
{
    int divisor{};
    std::cin >> divisor;
    std::cout << divide(100, divisor) << "\n";
    return 0;
}
