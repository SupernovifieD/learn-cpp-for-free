#include <bitset>
#include <iostream>

int main()
{
    const int columns{4};
    const int rows{2};
    std::bitset<columns * rows> grid{0b1010'0101};

    std::cout << grid << "\n";
    return 0;
}
