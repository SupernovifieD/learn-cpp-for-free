#include <iostream>

int main()
{
    constexpr int seatsPerRow{12};
    constexpr int rows{5};
    constexpr int totalSeats{seatsPerRow * rows};

    std::cout << "Seats booked: ";
    int booked{};
    std::cin >> booked;

    const int seatsLeft{totalSeats - booked};
    std::cout << "Seats in the hall: " << totalSeats << "\n";
    std::cout << "Seats left: " << seatsLeft << "\n";
    return 0;
}
