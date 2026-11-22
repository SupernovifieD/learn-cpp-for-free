#include <iostream>

int subtotal(int unitPrice, int count)
{
    return unitPrice * count;
}

int shipping(int goods)
{
    return goods / 10 + 4;
}

int main()
{
    int goods{subtotal(12, 4)};
    int delivery{shipping(goods)};
    std::cout << "Pay " << goods + delivery << "\n";
    return 0;
}
