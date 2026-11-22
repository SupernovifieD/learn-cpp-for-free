#include <iomanip>
#include <iostream>

int main()
{
    float shortThird{1.0f / 3.0f};
    double longThird{1.0 / 3.0};

    std::cout << std::setprecision(9) << shortThird << "\n";
    std::cout << std::setprecision(17) << longThird << "\n";
    return 0;
}
