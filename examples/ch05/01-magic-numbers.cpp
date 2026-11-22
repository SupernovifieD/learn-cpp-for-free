#include <iostream>

int main()
{
    int nights{3};
    int tents{2};

    std::cout << "Pitch fees: " << nights * tents * 25 << "\n";
    std::cout << "Deposit: " << 25 << "\n";
    return 0;
}
