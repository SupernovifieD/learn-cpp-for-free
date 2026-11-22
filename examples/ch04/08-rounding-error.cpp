#include <iomanip>
#include <iostream>

int main()
{
    double tenth{0.1};
    double sum{0.1 + 0.2};

    std::cout << std::setprecision(17);
    std::cout << "0.1 is stored as " << tenth << "\n";
    std::cout << "0.1 + 0.2 is " << sum << "\n";
    return 0;
}
