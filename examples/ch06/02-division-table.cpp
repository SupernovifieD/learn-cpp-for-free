#include <iostream>

void printRow(int number)
{
    std::cout << number << " " << number / 4 << " " << number / 4.0 << "\n";
}

int main()
{
    printRow(-7);
    printRow(-4);
    printRow(4);
    printRow(7);
    return 0;
}
