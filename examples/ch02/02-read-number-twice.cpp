#include <iostream>

int readNumber()
{
    int value{};
    std::cout << "Enter a number: ";
    std::cin >> value;
    return value;
}

int main()
{
    int first{readNumber()};
    int second{readNumber()};

    std::cout << "You entered " << first << " and " << second << ".\n";
    return 0;
}
