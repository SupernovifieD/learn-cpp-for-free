#include <iostream>

int main()
{
    int balance{100};
    balance = balance + 50;
    balance = balance - 30;
    balance = balance * 2;
    std::cout << "Balance: " << balance << "\n";
    return 0;
}
