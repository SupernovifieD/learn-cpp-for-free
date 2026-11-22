#include <iostream>

int main()
{
    std::cout << "Seats sold: ";
    int seatsSold{};
    std::cin >> seatsSold;

    std::cout << "Number of shows: ";
    int shows{};
    std::cin >> shows;

    if (shows <= 0)
    {
        std::cout << "There must be at least one show\n";
        return 1;
    }

    double average{static_cast<double>(seatsSold) / shows};
    std::cout << "Average seats per show: " << average << "\n";
    return 0;
}
