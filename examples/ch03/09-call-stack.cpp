#include <iostream>

int boxArea(int width, int height)
{
    return width * height;
}

int roomCost(int length, int width, int rate)
{
    int area{boxArea(length, width)};
    return area * rate;
}

int quote(int length, int width)
{
    int rate{3};
    int extra{20};
    int cost{roomCost(length, width, rate)};
    return cost + extra;
}

int main()
{
    int total{quote(5, 4)};
    std::cout << "Total: " << total << "\n";
    return 0;
}
