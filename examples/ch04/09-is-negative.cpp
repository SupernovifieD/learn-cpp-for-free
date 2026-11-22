#include <iostream>

bool isNegative(int number)
{
    return number < 0;
}

int main()
{
    std::cout << std::boolalpha;
    std::cout << "isNegative(-4): " << isNegative(-4) << "\n";
    std::cout << "isNegative(0): " << isNegative(0) << "\n";
    std::cout << "isNegative(9): " << isNegative(9) << "\n";
    return 0;
}
