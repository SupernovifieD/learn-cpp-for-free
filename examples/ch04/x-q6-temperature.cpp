#include <iostream>

int main()
{
    std::cout << "Enter the temperature: ";
    int degrees{};
    std::cin >> degrees;

    if (degrees < 0)
    {
        std::cout << "Freezing\n";
    }
    else if (degrees < 15)
    {
        std::cout << "Cold\n";
    }
    else if (degrees < 25)
    {
        std::cout << "Mild\n";
    }
    else
    {
        std::cout << "Warm\n";
    }
    return 0;
}
