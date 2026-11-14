#include <iostream>

void printLine()
{
    std::cout << "----\n";
}

void printTitle()
{
    printLine();
    std::cout << "Daily report\n";
    printLine();
}

int main()
{
    std::cout << "start of main\n";
    printTitle();
    std::cout << "middle of main\n";
    printTitle();
    std::cout << "end of main\n";
    return 0;
}
