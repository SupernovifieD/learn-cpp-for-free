#include <iostream>

int main()
{
    bool lampOn{};
    bool doorOpen{};

    std::cout << "Is the lamp on (0 or 1)? ";
    std::cin >> lampOn;

    std::cout << "Is the door open (true or false)? ";
    std::cin >> std::boolalpha >> doorOpen;

    std::cout << std::boolalpha;
    std::cout << "Lamp: " << lampOn << ", door: " << doorOpen << "\n";
    return 0;
}
