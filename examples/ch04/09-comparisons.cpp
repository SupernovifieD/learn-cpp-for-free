#include <iostream>

int main()
{
    int seats{30};
    int sold{24};

    std::cout << std::boolalpha;
    std::cout << "seats == sold: " << (seats == sold) << "\n";
    std::cout << "seats != sold: " << (seats != sold) << "\n";
    std::cout << "seats > sold: " << (seats > sold) << "\n";
    std::cout << "seats < sold: " << (seats < sold) << "\n";
    std::cout << "seats >= 30: " << (seats >= 30) << "\n";
    std::cout << "seats <= 29: " << (seats <= 29) << "\n";
    std::cout << "0.1 + 0.2 == 0.3: " << (0.1 + 0.2 == 0.3) << "\n";
    return 0;
}
