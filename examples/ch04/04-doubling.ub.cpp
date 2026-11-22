// undefined-behavior: signed overflow when a large int is doubled
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int number{};
    std::cin >> number;

    int doubled{number * 2};
    std::cout << "Twice that is " << doubled << "\n";
    return 0;
}
