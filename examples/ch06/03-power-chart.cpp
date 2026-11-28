#include <iostream>

void printPower(int exponent, int power)
{
    std::cout << exponent << " " << power << "\n";
}

int main()
{
    int power{1};
    printPower(0, power);
    power *= 2;
    printPower(1, power);
    power *= 2;
    printPower(2, power);
    power *= 2;
    printPower(3, power);
    power *= 2;
    printPower(4, power);
    power *= 2;
    printPower(5, power);
    power *= 2;
    printPower(6, power);
    power *= 2;
    printPower(7, power);
    power *= 2;
    printPower(8, power);
    power *= 2;
    printPower(9, power);
    power *= 2;
    printPower(10, power);
    return 0;
}
