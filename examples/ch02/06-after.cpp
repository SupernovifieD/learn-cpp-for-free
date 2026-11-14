#include <iostream>

void printCost(int amount, int price)
{
    std::cout << "  amount: " << amount << "\n";
    std::cout << "  cost: " << amount * price << " euros\n";
}

int main()
{
    std::cout << "Tea\n";
    printCost(2, 3);

    std::cout << "Coffee\n";
    printCost(1, 4);

    std::cout << "Cake\n";
    printCost(3, 5);
    return 0;
}
