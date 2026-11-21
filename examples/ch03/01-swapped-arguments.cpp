#include <iostream>

int priceAfterDiscount(int price, int discount)
{
    return price - discount;
}

int main()
{
    int ticketPrice{40};
    int voucher{5};
    std::cout << "You pay " << priceAfterDiscount(voucher, ticketPrice) << "\n";
    return 0;
}
