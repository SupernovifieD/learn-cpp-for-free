#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int number{};
    std::cin >> number;

    if (number < 0)
    {
        std::cout << number << " is negative\n";
    }
    else if (number == 0)
    {
        std::cout << "The number is zero\n";
    }
    else
    {
        std::cout << number << " is positive\n";
    }
    return 0;
}
