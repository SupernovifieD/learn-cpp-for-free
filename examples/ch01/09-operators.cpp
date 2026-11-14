#include <iostream>

int main()
{
    int seats{40};
    int reserved{12};

    std::cout << "free seats: " << seats - reserved << "\n";
    std::cout << "twice the seats: " << seats * 2 << "\n";
    std::cout << "opposite of reserved: " << -reserved << "\n";
    std::cout << "seats shared by 3: " << seats / 3 << "\n";
    std::cout << "2 + 3 * 4 is " << 2 + 3 * 4 << "\n";
    std::cout << "(2 + 3) * 4 is " << (2 + 3) * 4 << "\n";
    return 0;
}
