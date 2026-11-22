#include <iostream>

#define ENABLE_DEBUG

int seatTotal(int rows, int seatsPerRow)
{
#ifdef ENABLE_DEBUG
    std::cerr << "[debug] seatTotal(" << rows << ", " << seatsPerRow << ")\n";
#endif
    return rows * seatsPerRow;
}

int main()
{
    int total{seatTotal(12, 18)};
    std::cout << "Seats: " << total << "\n";
    return 0;
}
