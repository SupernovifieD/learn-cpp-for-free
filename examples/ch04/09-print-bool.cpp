#include <iostream>

int main()
{
    bool lampOn{true};
    bool doorOpen{false};

    std::cout << "Lamp: " << lampOn << ", door: " << doorOpen << "\n";

    std::cout << std::boolalpha;
    std::cout << "Lamp: " << lampOn << ", door: " << doorOpen << "\n";
    std::cout << "Lamp off: " << !lampOn << "\n";

    std::cout << std::noboolalpha;
    std::cout << "Lamp off: " << !lampOn << "\n";
    return 0;
}
