#include <iostream>

int ticketCount(int adults, int children)
{
    return adults + children;
}

int baseCost(int tickets, int price)
{
    return tickets * price;
}

int serviceFee(int cost)
{
    return cost / 10;
}

int totalCost(int cost, int fee)
{
    return cost + fee;
}

int main()
{
    int tickets{ticketCount(2, 3)};
    int cost{baseCost(tickets, 20)};
    int fee{serviceFee(cost)};
    std::cout << "Total: " << totalCost(cost, fee) << "\n";
    return 0;
}
