#include <iomanip>
#include <iostream>

int main()
{
    double measurement{12.3456789012345};

    std::cout << measurement << "\n";
    std::cout << std::setprecision(3) << measurement << "\n";
    std::cout << std::setprecision(12) << measurement << "\n";
    std::cout << 100.0 / 3.0 << "\n";
    return 0;
}
