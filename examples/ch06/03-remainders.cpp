#include <cmath>
#include <iostream>

int main()
{
    std::cout << std::boolalpha;
    std::cout << "-8 % 3 = " << -8 % 3 << "\n";
    std::cout << "8 % -3 = " << 8 % -3 << "\n";
    std::cout << "-8 % -3 = " << -8 % -3 << "\n";

    constexpr int value{-7};
    std::cout << value << " is odd: " << (value % 2 != 0) << "\n";

    constexpr int base{2};
    constexpr int exponent{3};
    std::cout << "2 ^ 3 = " << (base ^ exponent) << "\n";
    std::cout << "2 to the 3 = " << static_cast<int>(std::pow(2, 3)) << "\n";
    return 0;
}
