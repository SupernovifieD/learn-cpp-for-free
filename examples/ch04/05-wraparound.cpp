#include <iostream>

int main()
{
    unsigned int stock{0};
    std::cout << "Stock: " << stock << "\n";

    stock = stock - 1;
    std::cout << "After selling one more: " << stock << "\n";

    stock = stock + 1;
    std::cout << "After restocking one: " << stock << "\n";
    return 0;
}
