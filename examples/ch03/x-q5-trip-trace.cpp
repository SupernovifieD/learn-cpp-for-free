#include <iostream>

int tripCost(int distance, int ratePerUnit)
{
    std::cerr << "[debug] tripCost called\n";
    return distance * ratePerUnit;
}

int main()
{
    int cost{tripCost(40, 3)};
    std::cout << "Trip cost: " << cost << "\n";
    return 0;
}
