#include <iostream>

void printBanner()
{
    std::cout << "=====================\n";
    std::cout << "  Library opening\n";
    std::cout << "=====================\n";
}

int main()
{
    printBanner();
    std::cout << "Doors open at nine.\n";
    printBanner();
    return 0;
}
