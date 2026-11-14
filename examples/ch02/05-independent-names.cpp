#include <iostream>

void printInside()
{
    int level{2};
    std::cout << "level in printInside: " << level << "\n";
}

int main()
{
    int level{1};
    printInside();
    std::cout << "level in main: " << level << "\n";
    return 0;
}
