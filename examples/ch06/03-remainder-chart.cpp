#include <iostream>

void printRemainder(int value)
{
    std::cout << value << " " << value % 3 << "\n";
}

int main()
{
    printRemainder(-5);
    printRemainder(-4);
    printRemainder(-3);
    printRemainder(-2);
    printRemainder(-1);
    printRemainder(0);
    printRemainder(1);
    printRemainder(2);
    printRemainder(3);
    printRemainder(4);
    printRemainder(5);
    return 0;
}
