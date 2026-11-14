#include <iostream>

int main()
{
    int first{};
    int second{};

    std::cout << "Enter two numbers: ";
    std::cin >> first >> second;
    std::cout << "In reverse order: " << second << " " << first << "\n";
    return 0;
}
