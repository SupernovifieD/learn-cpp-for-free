// expect-fail: a call to an ordinary function is not a constant expression
#include <bitset>
#include <cstddef>
#include <iostream>

std::size_t columnCount()
{
    return 8;
}

int main()
{
    std::bitset<columnCount()> row{5};
    std::cout << row << "\n";
    return 0;
}
