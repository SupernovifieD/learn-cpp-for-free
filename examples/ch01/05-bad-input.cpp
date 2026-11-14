#include <iostream>

int main()
{
    int first{7};
    int second{9};

    std::cout << "Enter two numbers: ";
    std::cin >> first;
    std::cin >> second;
    std::cout << "first: " << first << "\n";
    std::cout << "second: " << second << "\n";
    return 0;
}
