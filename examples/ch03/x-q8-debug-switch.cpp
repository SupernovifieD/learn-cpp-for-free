#include <iostream>

#define ENABLE_DEBUG

int tripCost(int distance, int ratePerUnit)
{
#ifdef ENABLE_DEBUG
    std::cerr << "[debug] tripCost called\n";
#endif
    return distance * ratePerUnit;
}

int main()
{
    int cost{tripCost(40, 3)};
    std::cout << "Trip cost: " << cost << "\n";
    return 0;
}
