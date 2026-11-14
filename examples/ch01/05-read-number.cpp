#include <iostream>

int main()
{
    int bookCount{};

    std::cout << "How many books do you own? ";
    std::cin >> bookCount;
    std::cout << "You own " << bookCount << " books.\n";
    return 0;
}
