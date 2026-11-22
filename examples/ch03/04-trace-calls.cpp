#include <iostream>

int addShipping(int price)
{
    std::cerr << "[debug] addShipping called\n";
    return price + 5;
}

int addTax(int price)
{
    std::cerr << "[debug] addTax called\n";
    return price + price / 10;
}

void printReceipt(int price)
{
    std::cerr << "[debug] printReceipt called\n";
    std::cout << "Receipt total: " << price << "\n";
}

int main()
{
    int price{50};
    price = addShipping(price);
    printReceipt(price);
    return 0;
}
