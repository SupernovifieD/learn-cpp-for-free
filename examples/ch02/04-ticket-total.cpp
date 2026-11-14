#include <iostream>

int totalPrice(int tickets, int pricePerTicket)
{
    return tickets * pricePerTicket;
}

int main()
{
    int ticketCount{};
    int price{};

    std::cout << "How many tickets? ";
    std::cin >> ticketCount;
    std::cout << "Price per ticket in euros? ";
    std::cin >> price;

    std::cout << "Total: " << totalPrice(ticketCount, price) << " euros\n";
    return 0;
}
