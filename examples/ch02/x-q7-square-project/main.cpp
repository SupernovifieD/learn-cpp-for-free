#include "square.h"

#include <iostream>

int main()
{
    int side{};
    std::cout << "Side length: ";
    std::cin >> side;

    std::cout << "Area: " << squareArea(side) << "\n";
    std::cout << "Perimeter: " << squarePerimeter(side) << "\n";
    return 0;
}
