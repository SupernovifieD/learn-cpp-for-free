#include <iostream>

int percentOf(int part, int whole)
{
    return part * 100 / whole;
}

int main()
{
    int seatsSold{30};
    int seatsTotal{120};
    std::cout << "Sold: " << percentOf(seatsSold, seatsTotal) << " percent\n";
    return 0;
}
