// undefined-behavior: doubling a large number overflows an int
#include <iostream>

int main()
{
    int number{};
    std::cin >> number;
    std::cout << number * 2 << "\n";
    return 0;
}
