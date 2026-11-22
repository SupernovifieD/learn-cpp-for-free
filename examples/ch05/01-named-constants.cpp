#include <iostream>

int main()
{
    const int pitchFee{25};
    const int deposit{25};

    int nights{3};
    int tents{2};

    std::cout << "Pitch fees: " << nights * tents * pitchFee << "\n";
    std::cout << "Deposit: " << deposit << "\n";
    return 0;
}
