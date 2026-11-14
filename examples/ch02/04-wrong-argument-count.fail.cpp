// expect-fail: the call has one argument, but the function needs two
#include <iostream>

int totalPrice(int tickets, int pricePerTicket)
{
    return tickets * pricePerTicket;
}

int main()
{
    std::cout << totalPrice(3) << "\n";
    return 0;
}
