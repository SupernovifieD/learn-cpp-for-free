#include <iostream>

int main()
{
    std::cout << "How many seats are left? ";
    int seatsLeft{};
    std::cin >> seatsLeft;

    if (seatsLeft > 0)
    {
        std::cout << "Tickets are available\n";
    }
    else
    {
        std::cout << "Sold out\n";
    }

    std::cout << "Thank you for asking\n";
    return 0;
}
