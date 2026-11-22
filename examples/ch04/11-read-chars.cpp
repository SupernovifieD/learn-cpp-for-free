#include <iostream>

int main()
{
    char first{};
    char second{};

    std::cout << "First letter: ";
    std::cin >> first;
    std::cout << "Got: " << first << "\n";

    std::cout << "Second letter: ";
    std::cin >> second;
    std::cout << "Got: " << second << "\n";
    return 0;
}
