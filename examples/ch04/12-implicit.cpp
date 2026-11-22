#include <iostream>

void showAmount(double amount)
{
    std::cout << "Amount: " << amount << "\n";
}

int main()
{
    int cups{3};
    double total{0.5};

    total = cups;
    std::cout << "Total: " << total << "\n";

    showAmount(cups);
    return 0;
}
