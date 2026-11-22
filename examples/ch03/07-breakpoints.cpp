#include <iostream>

int applyDiscount(int price, int percent)
{
    return price - price * percent / 100;
}

int main()
{
    int first{applyDiscount(200, 10)};
    int second{applyDiscount(80, 25)};
    int third{applyDiscount(50, 50)};
    std::cout << first << " " << second << " " << third << "\n";
    return 0;
}
